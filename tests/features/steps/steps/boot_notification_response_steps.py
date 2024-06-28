from behave import then

@then('the CSMS should respond with a BootNotificationResponse "{response}" as response')
def step_impl(context, response):
    """Verify that the expected response is received."""
    for cp_info in context.charge_points:
        assert "response" in cp_info, "No response received"
        if hasattr(cp_info["response"], 'status'):
            assert cp_info["response"].status == response, f"Expected {response} but got {cp_info['response'].status}"
