import os
import sys
import logging
import argparse
import asyncio
from utils import Config
from utils import setup_logger
from websockets_kafka_bridge import WebSocketKafkaBridge


async def main():
    """
    This is the main function that initializes the ocpp-gw instance and
    starts the WebSocket server.
    """
    parser = argparse.ArgumentParser(description="Gateway Script")
    parser.add_argument("--config", default="./config.cfg", help="Config file path")
    parser.add_argument("--log_file", default="./ocpp_gw.log", help="Log file path")
    parser.add_argument("--log_level", default="INFO", help="Log level")
    args = parser.parse_args()

    if not os.path.exists(args.config):
       print(f"Config file '{args.config}' not found.")
       parser.print_usage()
       exit(1)
 
    # Config and Logger
    config = Config(args.config)
    logger = setup_logger(args.log_file, 
                          args.log_level, 
			  'ocpp_gw', 
			  max_size = 2_000_000, 
			  backups = 2) 
    logger.info("OCPP GW application started...")
    bridge = WebSocketKafkaBridge(config)
    asyncio.run(await bridge.run())

################################################################################
if __name__ == "__main__":
   try:
      asyncio.run(main())
   except KeyboardInterrupt:
      print("Exiting ...")

