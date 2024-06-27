import os
import sys
import json
import logging
import websockets
from websockets.server import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK
from utils import Config

logger = logging.getLogger('ocpp_gw')

class WebSocketHandler:
    """
    WebSocketHandler class is responsible for handling WebSocket connections,
    receiving and sending messages from/to the clients.
    """

    ###########################################################################
    def __init__(self, config: Config):
        """
        Initializes the WebSocketHandler with the provided configuration.

        Args:

            config (Config): The Configuration object containing WebSocket
            settings.
        """

        self.host = config.get("ocpp_gateway", "listening_host")
        self.port = config.get("ocpp_gateway", "listening_port")
        self.subprotocols = config.get("ocpp_gateway","subprotocols").split(",")
        self.clients = {}
        logger.info("WSH: WebSocket server initialized. "
                 f"host: {self.host} "
                 f"port: {self.port}")

    ###########################################################################
    async def websocket_handler(self, websocket: WebSocketServerProtocol,
                                path: str):
        """
        Handles the WebSocket connection and incoming messages and call the
        on_websocket_message_received method to handle the messages.

        Args:
            websocket (WebSocketServerProtocol): The WebSocket connection object.
            path (str): The path of the WebSocket connection.
        """
        # Extract the charge_point_id from the path and
        charge_point_id = path.strip("/")

        logger.info(f"WSH: Connection Request. "
                 f"charge_point_id: {charge_point_id}")

        # Verify protocols compatibility
        if "Sec-WebSocket-Protocol" not in websocket.request_headers:
            logger.info("WSH: Closing Connection - No subprotocol requestd! "
                     f"charge_point_id: {charge_point_id}")
            
            return await websocket.close()

        requested_protocols = websocket.request_headers["Sec-WebSocket-Protocol"]
        if not websocket.subprotocol:
            logger.error("WSH: Closing Connection - Protocols Mismatched! "
                      f"charge_point_id: {charge_point_id} "
                      f"Supported: {websocket.available_subprotocols} "
                      f"Requested: {requested_protocols}")
        
            return await websocket.close()

        # Save the client with the given charge_point_id
        self.clients[charge_point_id] = websocket

        # Call subclass method to handle the message.
        try:

            async for message in websocket:
                await self.on_websocket_message_received(
                        websocket,
                        message,
                        charge_point_id)

        except ConnectionClosedError as e:
            logger.error(f"Connection closed with error: {e}")
        except ConnectionClosedOK:
            logger.info("Connection closed normally")
        except asyncio.IncompleteReadError as e:
            logger.error(f"Incomplete read error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        finally:
            logger.info("WSH: Client disconnected. "
                     f"charge_point_id: {charge_point_id}")
            del self.clients[charge_point_id]

    ###########################################################################
    async def send_message_to_client(self, message: str, charge_point_id: str):
        """
        Send the message to connected client with the given charge_point_id.

        Args:
            charge_point_id (str): The ID of the client to send the message to.
            message (str): The message to send to the client.
        """
        # Get the client with the given charge_point_id
        client = self.clients.get(charge_point_id)
        if client:
            await client.send(message)

    ###########################################################################
    async def on_websocket_message_received(self,
                            websocket: WebSocketServerProtocol,
                            message: str, charge_point_id: str):
        """
        This method must be implemented in subclasses to handle the message
        coming from WebSocket.
        """
        raise NotImplementedError(
            "on_websocket_message_received method"
            "must be implemented in subclasses.")

    ###########################################################################
    async def wait_websocket_messages(self):
        """
        Start the WebSocket server.
        """
        server = await websockets.serve(
                    self.websocket_handler,
                    self.host,
                    self.port,
                    subprotocols=self.subprotocols)

        await server.wait_closed()
        logger.info("WSH: WebSocket server closed")
