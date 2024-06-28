import asyncio
from behave import when

@when('the Charging Station sends a Heartbeat request to the CSMS each "{interval}" seconds')
def step_then_start_sending_heartbeats_request(context, interval):
    """Start sending Heartbeat request messages for the specified interval."""
    async def start_heartbeats(cp_info):
        cp_info["charge_point"].heartbeat_task = context.loop.create_task(cp_info["charge_point"].start_heartbeats())
        await asyncio.sleep(int(interval))
        await cp_info["charge_point"].stop()

    for cp_info in context.charge_points:
        context.loop.run_until_complete(start_heartbeats(cp_info))
