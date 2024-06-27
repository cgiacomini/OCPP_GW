import asyncio
import logging
from aiohttp import WSMsgType

class WebSocketWrapper:
    def __init__(self, ws):
        """Initialize the WebSocket wrapper."""
        self._ws = ws
        self._recv_task = None  # To store the receive task

    async def send(self, message):
        """Send a message over the WebSocket."""
        logging.debug(f"Sending message: {message}")
        await self._ws.send_str(message)

    async def recv(self):
        """Receive a message from the WebSocket."""
        if self._recv_task is None or self._recv_task.done():
            self._recv_task = asyncio.create_task(self._receive_task())
        return await self._recv_task

    async def _receive_task(self):
        """Handle receiving messages from the WebSocket."""
        msg = await self._ws.receive()
        if msg.type == WSMsgType.TEXT:
            logging.debug(f"Received message: {msg.data}")
            return msg.data
        elif msg.type == WSMsgType.BINARY:
            logging.debug("Received binary message")
            return msg.data
        elif msg.type == WSMsgType.CLOSED:
            logging.debug("WebSocket closed")
            await self._ws.close()
            return None
        elif msg.type == WSMsgType.ERROR:
            logging.debug("WebSocket error")
            return None

    async def close(self):
        """Close the WebSocket connection."""
        await self._ws.close()
