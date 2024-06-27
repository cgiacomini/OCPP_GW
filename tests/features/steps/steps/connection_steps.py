import asyncio
from behave import given
from aiohttp import ClientSession
from utils.websocket_wrapper import WebSocketWrapper
from utils.charge_point import ChargePoint

SERVER_URL = "ws://localhost:9000"

@given('I have a charging station with unique_id "{unique_id}" and subprotocol "{subprotocol}" connected to the server')
def step_given_charging_station_connected(context, unique_id, subprotocol):
    """Connect the charging station to the server with the given unique ID and subprotocol."""
    async def connect():
        session = ClientSession()
        ws = await session.ws_connect(
            f"{SERVER_URL}/{unique_id}",
            protocols=[subprotocol]
        )
        ws_wrapper = WebSocketWrapper(ws)
        charge_point = ChargePoint(unique_id, ws_wrapper, subprotocol)
        connected = True

        # Storing in context
        if not hasattr(context, "charge_points"):
            context.charge_points = []
        context.charge_points.append({
            "session": session,
            "ws": ws_wrapper,
            "charge_point": charge_point,
            "connected": connected,
            "start_task": None
        })

    context.loop = asyncio.get_event_loop()
    context.loop.run_until_complete(connect())
