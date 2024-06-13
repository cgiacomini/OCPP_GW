import os
import sys
import json
import asyncio
import logging
import ocpp.messages
from confluent_kafka import Producer, Consumer, KafkaException, KafkaError
from utils import Config

logger = logging.getLogger('ocpp_gw')


class KafkaHandler:
    """ 
    The KafkaHandler class that handles Kafka consumer and producer.
    """
    
    ############################################################################
    def __init__(self, config: Config):
        """
        Initialize the Kafka consumer and producer with the given configuration.
        """
        self.kafka_servers = config.get("kafka", "servers")
        self.consumer_group = config.get("kafka", "ocpp_gw_consumer_group")
        self.auto_offset_reset = config.get("kafka", "auto_offset_reset")
        self.to_csms_topic = config.get("kafka", "in_messages_topic")
        self.to_cp_topic = config.get("kafka", "out_messages_topic")

        self.consumer_conf = {
            'bootstrap.servers': self.kafka_servers,
            'group.id': self.consumer_group,
            'auto.offset.reset': self.auto_offset_reset,
        }
        self.producer_conf = {
            'bootstrap.servers': self.kafka_servers,
        }

        self.consumer = Consumer(self.consumer_conf)
        self.producer = Producer(self.producer_conf)
        self.consumer.subscribe([self.to_cp_topic])
        logger.info("KFH: Kafka consumer and producer initialized. "
                   f"servers: {self.kafka_servers}")

    ############################################################################
    def delivery_report(self, err: KafkaError, msg: any ):
        """Called once for each message produced to indicate delivery result."""
        if err is not None:
            logger.info("KFH: Message delivery to CSMS failed. "
                      f"Error: {err} "
                      f"msg_value: {msg.value()}")
        else:
            logger.info("KFH: Message delivered to CSMS. "
                     f"msg_value: {msg.value()}")
             
    ############################################################################
    async def produce_message(self, message, headers=None):
        """ Produce a kafka message to the to_csms_topic. """
        try:
            logger.info("KFH: Publishing message "
                     f"msg_headers: {headers} "
                     f"msg_value: {ocpp.messages.unpack(message)}")
            
            self.producer.produce(
                topic = self.to_csms_topic,
                value = message.encode('utf-8'),
                headers = headers,
                on_delivery = self.delivery_report)
            self.producer.poll()

        except KafkaException as e:
            logger.error("KF: Failed to produce message. "
                      f"error: {e} "
                      f"topic: {self.to_csms_topic} "
                      f"msg_headers: {headers} "
                      f"msg_value: {message}")

    ############################################################################
    async def wait_kafka_messages(self):
        """
        Consume messages from subscribed the Kafka topic and call the 
        on_kafka_message_received method to handle the message.
        """
        try:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    await asyncio.sleep(1)  # Avoid tight loop if no message
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        logger.error("KFH: End of partition reached. "
                                  f"{msg.topic()}/{msg.partition()}")
                        continue
                    logger.error(f"KFH: Kafka Consumer error: {msg.error()}")
                    continue

                # Extract message from value
                message = msg.value().decode('utf-8')
                # Extract client_id from headers
                charge_point_id = dict(msg.headers())['charge_point_id'].decode('utf-8')
                ocpp_message = ocpp.messages.unpack(message)

                logger.info("KFH:  Message consumed. "
                    f"topic: {msg.topic()} "
                    f"msg_value: {ocpp_message} "
                    f"msg_headers: {msg.headers()} ")

                # Call subclass method to handle the message.
                await self.on_kafka_message_received(message, charge_point_id)

        except asyncio.CancelledError:
            pass
        finally:
            self.consumer.close()

    ############################################################################
    async def on_kafka_message_received(self, message, charge_point_id):
        """ 
        This method must be implemented in subclasses to handle the message
        coming from Kafka topic.
        
        Raises:
            NotImplementedError: If the method is not implemented in subclasses.
        """
        raise NotImplementedError(
            "on_kafka_message_received method"
            "must be implemented in subclasses.")

