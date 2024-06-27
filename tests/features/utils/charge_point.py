# charge_point/charge_point.py

import logging
import asyncio
from ocpp.v201 import ChargePoint as cp_v201
from ocpp.v201 import call as call_v201
from ocpp.v16 import ChargePoint as cp_v16
from ocpp.v16 import call as call_v16

class ChargePoint:
    def __init__(self, unique_id, ws, protocol):
        """Initialize the ChargePoint with the given unique ID, WebSocket, and protocol."""
        self.protocol = protocol
        self.unique_id = unique_id
        self.heartbeat_task = None
        self.heartbeat_interval = None

        if protocol == "ocpp2.0.1":
            self.charge_point = cp_v201(unique_id, ws)
        elif protocol == "ocpp1.6":
            self.charge_point = cp_v16(unique_id, ws)
        else:
            raise ValueError(f"Unsupported protocol: {protocol}")

    async def send_boot_notification(self, vendor, model):
        """Send a BootNotification message with the given vendor and model."""
        if self.protocol == "ocpp2.0.1":
            request = call_v201.BootNotification(
                charging_station={
                    "model": model,
                    "vendor_name": vendor
                },
                reason="PowerUp",
            )
        elif self.protocol == "ocpp1.6":
            request = call_v16.BootNotification(
                charge_point_model=model,
                charge_point_vendor=vendor,
            )
        else:
            raise ValueError(f"Unsupported protocol: {self.protocol}")

        try:
            response = await self.charge_point.call(request)
            logging.info(f"Received response: {response}")
            self.heartbeat_interval = response.interval
            return response
        except Exception as e:
            logging.error(f"Error sending BootNotification: {e}")
            return None

    async def send_heartbeat(self):
        """Send a Heartbeat message."""
        if self.protocol == "ocpp2.0.1":
            request = call_v201.Heartbeat()
        elif self.protocol == "ocpp1.6":
            request = call_v16.Heartbeat()
        else:
            raise ValueError(f"Unsupported protocol: {self.protocol}")

        try:
            response = await self.charge_point.call(request)
            logging.info(f"Received Heartbeat response: {response}")
        except Exception as e:
            logging.error(f"Error sending Heartbeat: {e}")

    async def start_heartbeats(self):
        """Start sending Heartbeat messages at regular intervals."""
        while True:
            await self.send_heartbeat()
            await asyncio.sleep(self.heartbeat_interval)

    async def start(self):
        """Start the ChargePoint."""
        await self.charge_point.start()

    async def stop(self):
        """Stop the ChargePoint and cancel any running heartbeat tasks."""
        if self.heartbeat_task:
            self.heartbeat_task.cancel()
            try:
                await self.heartbeat_task
            except asyncio.CancelledError:
                pass
