
import os
import sys
import asyncio
import argparse
import ocpp.messages

from datetime import datetime
from typing import Any
from ocpp.v201.enums import Action, RegistrationStatusType
from ocpp.routing import on
from ocpp.v201 import ChargePoint as cp
from confluent_kafka import Producer, Consumer
from confluent_kafka.admin import  AdminClient, NewTopic
from utils import Config
from utils import setup_logger

# Globals
logger = None

################################################################################
class CSMS(cp):

    ############################################################################
    def __init__(self, config: Config):

        global logger
        self.config = config
        self.kafka_servers = self.config.get('kafka', 'servers')
        self.consumer_group= self.config.get('kafka', 'csms_consumer_group')
        self.auto_offset_reset = config.get("kafka", "auto_offset_reset")
        self.to_csms_topic = config.get("kafka", "in_messages_topic")
        self.to_cp_topic = config.get("kafka", "out_messages_topic")
        self.num_partitions = int(self.config.get('kafka', 'num_partitions'))
        self.replica_factor = int(self.config.get('kafka', 'replica_factor'))


        self.consumer_conf = {
            'bootstrap.servers': self.kafka_servers,
            'group.id': self.consumer_group,
            'auto.offset.reset': self.auto_offset_reset,
        }
        self.producer_conf = {
            'bootstrap.servers': self.kafka_servers,
        }

        self.consumer = Consumer(self.consumer_conf)
        self.consumer.subscribe([self.to_csms_topic])

        self.producer = Producer(self.producer_conf)
        self.admin_client = AdminClient(self.producer_conf)

        self._create_kafka_topic(
                            self.to_csms_topic,
                            self.num_partitions,
                            self.replica_factor)
        self._create_kafka_topic(
                            self.to_cp_topic,
                            self.num_partitions,
                            self.replica_factor)

        logger.info(f"Subscriber: for {self.to_csms_topic} topic")
        logger.info(f"Producer:   for {self.to_cp_topic} topic")

    ##############################################################################
    def _create_kafka_topic(self, topic_name: str, 
                            num_partitions: int, 
                            replication_factor: int):

        # Retrieve the metadata for all topics
        metadata = self.admin_client.list_topics(timeout=10)

        # Check if the topic exists in the metadata
        if topic_name in metadata.topics:
            logger.debug(f"Topic '{topic_name}' already exists.")
            return True

        logger.debug(f"Topic '{topic_name}' does not exist. Creating topic...")
        new_topic = NewTopic(topic_name, num_partitions, replication_factor)

        futures = self.admin_client.create_topics([new_topic])
        try:
            for topic, future in futures.items():
                try:
                    future.result()
                    logger.debug(f"Topic '{topic_name}' created successfully")
                    return True
                except Exception as e:
                    logger.error(f"Failed to create topic '{topic_name}': {e}")
                    return False
        except Exception as e:
            logger.error(f"Error while creating topic '{topic_name}': {e}")
            return False

    ##############################################################################
    async def process_message(self, msg: Any):

        charge_point_id = dict(msg.headers())['charge_point_id'].decode('utf-8')
        message = msg.value().decode('utf-8')

        # Unpack message to get Call object
        ocpp_message = ocpp.messages.unpack(message)

        try:
            action  = ocpp_message.action
            if action == Action.boot_notification:
                return await self.on_boot_notification(ocpp_message, charge_point_id = charge_point_id)
            elif action == Action.heartbeat:
                return await self.on_heartbeat(ocpp_message, charge_point_id = charge_point_id)
        except Exception as e:
            logger.error(f"Error while handling message: {e}")

    ################################################################################
    @on("Heartbeat")
    async def on_heartbeat(self, message, **kwargs):
        """ Handle Heartbeat message from Charge Point"""
        logger.info(f"Received Heartbeat: {message}")
        return message.create_call_result(
            {"currentTime":datetime.now().isoformat()}
    )
  
    ############################################################################
    @on("BootNotification")
    async def on_boot_notification(self, message, **kwargs):
        """ Handle BootNotification message from Charge Point """
        # Extract the charging_station_id from kwargs
        charge_point_id = kwargs.get('charge_point_id')

        logger.info(f"Received BootNotification: {message}")
        return_status = RegistrationStatusType.accepted

        if self._charge_point_exists(charge_point_id) is False:
            return_status = RegistrationStatusType.rejected

        return message.create_call_result(
            {
                "currentTime": datetime.now().isoformat(),
                "interval": 10,  # set default interval period in seconds
                "status": return_status,
            }
        )
  
    ############################################################################
    def _charge_point_exists(self, charge_point_id):
        """ Check if the charging station is known to the CSMS"""
        # Query a database for a list of configured charge points
        if not charge_point_id.startswith("CP_"):
            logger.error(f"Unknown Charge Point detected: {charge_point_id}")
            return False
        return True
  
    ############################################################################
    def delivery_report(self, err, msg):
        """Delivery report callback called on producing message"""
        if err is not None:
            logger.info(f'Message delivery failed: {err}')
        else:
            logger.info(f'Message delivered to topic: {msg.topic()} partition {msg.partition()} msg {msg.value()}')

    ##############################################################################
    async def consume_messages(self):

        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    await asyncio.sleep(0.1)  # Yield control to the event loop
                    continue
                if msg.error():
                    logger.error(f"Consumer error: {msg.error()}")
                    continue

                response = await self.process_message(msg)
               
                logger.info(
                    f"Message To Gateway. "
                    f"headers: {msg.headers()} message: {response}")

                self.producer.produce(
                     topic = self.to_cp_topic,
                     value = response.to_json().encode("utf-8"),
                     callback = self.delivery_report,
                     headers = msg.headers() # OCPPGateway will use this for routing to the good CP
                )
                self.producer.flush()

        except KeyboardInterrupt:
            logger.info("Stopping consumer")


################################################################################
async def main():
    """
    This is the main function that initializes the CSMS 
    """
    parser = argparse.ArgumentParser(description="Charge Point Management System")
    parser.add_argument("--config", default="./config.cfg", help="Config file path")
    parser.add_argument("--log_file", default="./csms.log", help="Log file path")
    parser.add_argument("--log_level", default="INFO", help="Log level")
    args = parser.parse_args()

    if not os.path.exists(args.config):
       print(f"Config file '{args.config}' not found.")
       parser.print_usage()
       exit(1)

    # Config and Logger
    config = Config(args.config)

    global logger
    logger = setup_logger(args.log_file,
                          args.log_level,
                          'ocpp',
                          max_size = 2_000_000,
                          backups = 2)

    csms = CSMS(config)
    logger.info("CSMS Started ...")
    asyncio.run(await csms.consume_messages())

################################################################################
if __name__ == "__main__":
   try:
      asyncio.run(main())
   except KeyboardInterrupt:
      print("Exiting ...")
