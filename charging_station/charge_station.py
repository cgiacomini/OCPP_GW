import os
import sys
import asyncio
import logging
import argparse
import websockets
from  websockets.exceptions import WebSocketException
from ocpp.v201 import ChargePoint as cp
from ocpp.v201 import call
from utils import Config
from utils import setup_logger

# Globals
logger = None

################################################################################
class ChargePoint(cp):
    async def send_heartbeat(self, interval):
        request = call.Heartbeat()
        while True:
            try:
                await self.call(request)
                await asyncio.sleep(interval)
            except asyncio.TimeoutError as e:
                logger.error(f"WebSocket timeout: {e}")
                pass
            except WebSocketException as e:
                logger.error(f"WebSocket error: {e}. Attempting to reconnect...")
                break  # Break to reconnect

    async def send_boot_notification(self):
        request = call.BootNotification(
            charging_station={"model": "Wallbox 123", "vendor_name": "anewone"},
            reason="PowerUp",
        )
        while True:
            try:
                response = await self.call(request)
                if response.status == "Accepted":
                    logger.info("Connected to central system.")
                    await self.send_heartbeat(response.interval)
            except WebSocketException as e:
                logger.error(f"WebSocket error: {e}. Attempting to reconnect...")
                break  # Break to reconnect

################################################################################
async def connect_and_run(config: Config, cp_id: str):
    while True:
        try:
            server_host = config.get('ocpp_gateway', 'host')
            listening_port = config.get('ocpp_gateway', 'listening_port')
            subprotocols = config.get('ocpp_gateway', 'subprotocols').split(',')

            async with websockets.connect(
                f"ws://{server_host}:{listening_port}/{cp_id}", 
                subprotocols=subprotocols
            ) as ws:
                charge_point = ChargePoint(cp_id, ws)
                await asyncio.gather(
                    charge_point.start(), charge_point.send_boot_notification()
                )
        except websockets.ConnectionClosed as e:
            logger.error(f"Connection lost: {e}. Reconnecting in 5 seconds...")
            await asyncio.sleep(5)  # Wait before attempting to reconnect
        except OSError as e:
            logger.error(f"OSError : {e}. Reconnecting in 5 seconds...")
            await asyncio.sleep(5)  # Wait before attempting to reconnect


################################################################################
async def main():
    # Create the parser
    parser = argparse.ArgumentParser(description='Process a cp_id parameter.')
    # Add parameter
    parser.add_argument("--config", default="./config.cfg", help="Config file path")
    parser.add_argument("--log_level", default="INFO", help="Log level")
    parser.add_argument('--cp_id', default="CP_1", help='The cp_id parameter as a string')

    # Parse the arguments
    args = parser.parse_args()
    if not os.path.exists(args.config):
       print(f"Config file '{args.config}' not found.")
       parser.print_usage()
       exit(1)

    config = Config(args.config)

    # Get the cp_id value
    cp_id = args.cp_id

    global logger
    logger = setup_logger(args.cp_id + ".log",
                          args.log_level,
                          "ocpp",
                          max_size = 2_000_000,
                          backups = 2)
    
    await connect_and_run(config, cp_id)


################################################################################
if __name__ == "__main__":
    asyncio.run(main())

