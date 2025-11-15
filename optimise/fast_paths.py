def fast_path_check(input_data: str):
    """Checks for simple inputs that can be answered without an LLM."""
    normalized_input = input_data.lower().strip()
    
    if normalized_input in ["hello", "hi", "hello iron man track!"]:
        return "Fast path response: Hello! How can I help you today?"
    
    if "thank you" in normalized_input:
        return "Fast path response: You're welcome!"

    return None # No fast path found
