import os
import sys
import json
import asyncio
import logging
import ocpp.messages
from ocpp.v201.enums import RegistrationStatusType
from kafka_handler  import KafkaHandler
from websockets_handler import WebSocketHandler
from utils import Config

logger = logging.getLogger('ocpp_gw')

################################################################################
class WebSocketKafkaBridge(KafkaHandler, WebSocketHandler):
    def __init__(self, config: Config):
        """
        Initialize the bridge with Kafka and WebSocket configurations.
        """
        KafkaHandler.__init__(self, config)
        WebSocketHandler.__init__(self, config)

    ############################################################################
    async def on_kafka_message_received(self, message, charge_point_id):
        """ 
        This method is called when a message is received from Kafka. 
        Is the implementation of the on_kafka_message_received's KafkaHandler 
        abstract method. 
        If received message has status rejected, close the WebSocket connection.
        """

        await self.send_message_to_client(message, charge_point_id)
        
        # We close connection if payload has status rejected
        ocpp_message = ocpp.messages.unpack(message)
        if "status" in ocpp_message.payload.keys() and \
           ocpp_message.payload["status"] == RegistrationStatusType.rejected:
           logger.error("WKB: Operation rejected! - Closing connection."
                     f"charge_point_id: {charge_point_id}") 

           client = self.clients.get(charge_point_id)
           if client:
               await client.close(reason="Server closing connection")

    ############################################################################
    async def on_websocket_message_received(self, websocket, message,
                                            charge_point_id):
        """
        This method is called when a message is received from WebSocket.
        Is the implementation of the WebSocketHandler abstract method.
        """
        headers = [('charge_point_id', charge_point_id)]
        await self.produce_message(message, headers)

    ############################################################################
    async def run(self):
        kafka_handler_task = asyncio.create_task(self.wait_kafka_messages())
        websockets_handler_task = asyncio.create_task(self.wait_websocket_messages())
        await asyncio.gather(kafka_handler_task, websockets_handler_task)
