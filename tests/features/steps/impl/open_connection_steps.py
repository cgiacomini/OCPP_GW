import asyncio
from behave import given
from aiohttp import ClientSession
from utils.websocket_wrapper import WebSocketWrapper
from utils.charge_point import ChargePoint

@given("a charging station with unique_id {unique_id} and subprotocol {subprotocol} connected to CSMS")
def step_impl(context, unique_id, subprotocol):
    """Connect the charging station to the server with the given unique ID and subprotocol."""
    async def connect():
        server_url = context.server_url
        session = ClientSession()
        ws = await session.ws_connect(
            f"{server_url}/{unique_id}",
            protocols=[subprotocol]
        )
        ws_wrapper = WebSocketWrapper(ws)
        charge_point = ChargePoint(unique_id, ws_wrapper, subprotocol)
        connected = True

        # # Storing in context
        if not hasattr(context, "charge_points"):
             context.charge_points = []
        context.charge_points.append({
            "session": session,
            "ws": ws_wrapper,
            "charge_point": charge_point,
            "connected": connected,
            "start_task": None,
            "connetors": [ {"connectorId": 1, "type": "Type2", "maxCurrent": 32, "voltage": 230, "status": "Unavailable"},
                           {"connectorId": 2, "type": "CCS2", "maxCurrent": 100, "voltage": 400, "status": "Unavailable"} ]
        })

    context.loop = asyncio.get_event_loop()
    context.loop.run_until_complete(connect())
