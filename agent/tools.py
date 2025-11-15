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
    """A small utility/tool that adds two numbers.

    Accepts numeric strings or numbers. Returns a tuple (sum, representation).
    The representation is a friendly string suitable for including in prompts.
    """
    logger.info(f"add_numbers called with: {a}, {b}")
    try:
        # Convert to float if contains a dot, otherwise int where possible
        def to_num(x):
            if isinstance(x, (int, float)):
                return x
            sx = str(x).strip()
            if '.' in sx:
                return float(sx)
            return int(sx)

        na = to_num(a)
        nb = to_num(b)
        result = na + nb
        # normalize int-like floats to int for nicer display
        if isinstance(result, float) and result.is_integer():
            result = int(result)

        rep = f"{na} + {nb} = {result}"
        logger.debug(f"add_numbers result: {rep}")
        return result, rep
    except Exception as e:
        logger.error(f"Failed to add numbers: {a}, {b} - {e}")
        raise
