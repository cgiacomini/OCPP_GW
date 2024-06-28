from behave import then
import logging


@then('the CSMS should respond with a HeartbeatResponse with the current time')
def step_impl(context):
    """Verify that the Heartbeat response contains the current time."""
    for cp_info in context.charge_points:
        # Access the ChargePoint instance
        charge_point = cp_info['charge_point']
        assert charge_point.heartbeat_response is not None, "No Heartbeat response received"
        logging.info(f"Heartbeat response: {charge_point.heartbeat_response}")
        assert hasattr(charge_point.heartbeat_response, 'current_time'), "Heartbeat response does not contain current time"
        current_time = charge_point.heartbeat_response.current_time
        logging.info(f"Heartbeat current time: {current_time}")
        cp_info['current_time'] = current_time
