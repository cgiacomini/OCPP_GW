import asyncio
from behave import when

@when('the Charging Station sends a Heartbeat request to the CSMS each "{interval}" seconds')
def step_impl(context, interval):
    """Start sending Heartbeat request messages for the specified interval."""
    async def start_heartbeats(cp_info):
        cp_info["charge_point"].heartbeat_task = context.loop.create_task(cp_info["charge_point"].start_heartbeats())
        await asyncio.sleep(int(interval))
        await cp_info["charge_point"].stop()

    for cp_info in context.charge_points:
        context.loop.run_until_complete(start_heartbeats(cp_info))

@when('the Charging Station sends an Heartbeat request to the CSMS')
def step_impl(context):
    """Sending an Heartbeat request messages to the CSMS."""
    async def send_heartbeat(cp_info):
        await cp_info["charge_point"].send_heartbeat()

    for cp_info in context.charge_points:
        context.loop.run_until_complete(send_heartbeat(cp_info))
