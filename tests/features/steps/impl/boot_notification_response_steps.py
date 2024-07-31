from behave import then

@then('the CSMS respond with BootNotificationResponse with status "{status}"')
def step_impl(context, status):
    """Verify that the expected response is received."""
    for cp_info in context.charge_points:
        assert "response" in cp_info, "No response received"
        if hasattr(cp_info["response"], 'status'):
            assert cp_info["response"].status == status, f"Expected {status} but got {cp_info['response'].status}"
