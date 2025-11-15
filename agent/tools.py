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
