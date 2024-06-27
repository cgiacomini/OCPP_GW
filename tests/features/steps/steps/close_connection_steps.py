import asyncio
from behave import then

@then('close the connection')
def step_then_close_connection(context):
    """Close the connection to the server."""
    async def close(cp_info):
        await cp_info["charge_point"].stop()
        # Ensure the start task is canceled and awaited
        cp_info["start_task"].cancel()
        try:
            await cp_info["start_task"]
        except asyncio.CancelledError:
            pass

        await cp_info["ws"].close()
        await cp_info["session"].close()

    for cp_info in context.charge_points:
        context.loop.run_until_complete(close(cp_info))
