import logging
import time

logger = logging.getLogger(__name__)

class LLMModel:
    """A dummy LLM model wrapper."""
    def __init__(self, model_name="stub-model"):
        self.model_name = model_name
        logger.info(f"LLMModel ({self.model_name}) initialized.")

    def query(self, prompt):
        """Simulates an LLM API call."""
        logger.debug(f"Querying model {self.model_name} with prompt: {prompt[:50]}...")
        time.sleep(0.1) # Simulate network latency
        return f"This is a dummy LLM response to '{prompt}'"

def execute_tool(plan: str):
    """
S    imulates executing a tool based on the agent's plan.
    """
    logger.info(f"Executing tool with plan: {plan}")
    
    # Simulate tool work
    time.sleep(0.2) # Simulate tool execution time
    
    if "fail" in plan.lower():
        # This allows the test_suite to trigger a failure
        raise ValueError("Tool execution failed as per plan.")
        
    tool_result = f"Tool successfully executed plan: '{plan}'"
    return tool_result


def add_numbers(a, b):
    """Add two or more numbers.

    Usage:
      add_numbers("2+3+4")
      add_numbers(2, 3, 4)
      add_numbers(["2", "3.5", 4])

    Returns (numeric_sum, representation_string) where representation_string is
    like "2 + 3 + 4 = 9".
    """
    logger.info(f"add_numbers called with: {a}, {b}")
    try:
        import re

        # Normalize inputs into a flat list of parts (strings or numbers)
        parts = []
        # If caller passed a single iterable as 'a' and b is missing/None
        if b is None and isinstance(a, (list, tuple)):
            parts = list(a)
        # If caller passed a single string expression like "2+3+4"
        elif b is None and isinstance(a, str) and '+' in a:
            parts = [p.strip() for p in re.split(r"\+", a) if p.strip()]
        else:
            # General case: combine provided positional args
            # Note: original signature had (a, b), but we support extra args
            provided = [a]
            if b is not None:
                provided.append(b)
            parts = provided

        def to_num(x):
            if isinstance(x, (int, float)):
                return x
            sx = str(x).strip()
            if '.' in sx:
                return float(sx)
            return int(sx)

        nums = [to_num(p) for p in parts]
        result = sum(nums)

        # normalize int-like floats to int for nicer display
        if isinstance(result, float) and result.is_integer():
            result = int(result)

        rep_parts = []
        for n in nums:
            # show ints without decimal point
            if isinstance(n, float) and n.is_integer():
                rep_parts.append(str(int(n)))
            else:
                rep_parts.append(str(n))

        rep = " + ".join(rep_parts) + f" = {result}"
        logger.debug(f"add_numbers result: {rep}")
        return result, rep
    except Exception as e:
        logger.error(f"Failed to add numbers: {a}, {b} - {e}")
        raise
