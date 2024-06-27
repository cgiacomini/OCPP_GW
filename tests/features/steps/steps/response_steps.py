from behave import then

@then('I should receive "{response}" as response')
def step_then_receive_accepted_response(context, response):
    """Verify that the expected response is received."""
    for cp_info in context.charge_points:
        assert "response" in cp_info, "No response received"
        if hasattr(cp_info["response"], 'status'):
            assert cp_info["response"].status == response, f"Expected {response} but got {cp_info['response'].status}"
