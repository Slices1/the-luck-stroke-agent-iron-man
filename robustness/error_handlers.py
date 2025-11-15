def handle_invalid_input(input_data):
    """Handles gracefully failing on bad input."""
    return f"Error: Input was invalid. Please rephrase. (Received: '{input_data}')"

def handle_tool_failure(exception, plan):
    """Handles a failed tool execution."""
    error_message = f"Error: The agent's tool failed. (Plan: {plan}, Error: {exception})"
    # In a real scenario, you might try a recovery plan here.
    # For Iron Man, a fast, stable failure is better than a crash.
    return error_message
