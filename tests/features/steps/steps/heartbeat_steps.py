import asyncio
from behave import then

@then('I start sending heartbeats for "{interval}" seconds')
def step_then_start_sending_heartbeats(context, interval):
    """Start sending Heartbeat messages for the specified interval."""
    async def start_heartbeats(cp_info):
        cp_info["charge_point"].heartbeat_task = context.loop.create_task(cp_info["charge_point"].start_heartbeats())
        await asyncio.sleep(int(interval))
        await cp_info["charge_point"].stop()

    for cp_info in context.charge_points:
        context.loop.run_until_complete(start_heartbeats(cp_info))
