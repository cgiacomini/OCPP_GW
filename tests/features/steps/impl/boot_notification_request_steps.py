import logging
from behave import when

@when('the Charging Station sends a BootNotification to the CSMS with vendor "{vendor}" and model "{model}"')
def step_impl(context, vendor, model):
    """Send a BootNotification message with the specified vendor and model."""
    async def send_boot_notification(cp_info):
        try:
            response = await cp_info["charge_point"].send_boot_notification(vendor, model)
            cp_info["response"] = response
        except Exception as e:
            logging.error(f"Error sending BootNotification: {e}")
            raise

    # Wait for the BootNotification response
    for cp_info in context.charge_points:
        cp_info["start_task"] = context.loop.create_task(cp_info["charge_point"].start())
        context.loop.run_until_complete(send_boot_notification(cp_info))
