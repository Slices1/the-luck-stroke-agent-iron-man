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
        logger.debug(f"Querying model {self.model_name} with prompt: {prompt[:120]}...")
        time.sleep(0.05) # Simulate network latency

        # Placeholder behaviour: if the prompt contains a simple addition
        # expression, instruct the controller to call the add_numbers tool.
        # The format used is: CALL_TOOL:add_numbers:2+3+4
        import re
        match = re.search(r"(-?\d+(?:\.\d+)?(?:\s*\+\s*-?\d+(?:\.\d+)?)+)", prompt)
        if match:
            expr = match.group(1)
            # normalize spaces around plus signs
            expr_clean = re.sub(r"\s+", "", expr)
            logger.debug(f"LLM stub detected arithmetic expression: {expr_clean}; returning CALL_TOOL plan")
            return f"CALL_TOOL:add_numbers:{expr_clean}"

        # Default dummy response
        return f"DUMMY_PLAN: Execute the plan for '{prompt}'"

def execute_tool(plan: str):
    """
S    imulates executing a tool based on the agent's plan.
    """
    logger.info(f"Executing tool with plan: {plan}")

    # If the plan is a CALL_TOOL directive, parse it and call the named tool.
    if isinstance(plan, str) and plan.startswith("CALL_TOOL:"):
        # Expected format: CALL_TOOL:tool_name:args
        parts = plan.split(":", 2)
        if len(parts) < 3:
            raise ValueError("Invalid CALL_TOOL plan format")
        tool_name = parts[1]
        tool_args = parts[2]

        # Map tool name to function
        if tool_name == "add_numbers":
            # tool_args could be "2+3+4" or "2,3,4". Prefer plus form.
            # Try to call add_numbers with the expression string so it can parse.
            try:
                result, rep = add_numbers(tool_args)
                return f"TOOL_RESULT:add_numbers:{rep}"
            except Exception as e:
                logger.error(f"add_numbers tool failed: {e}")
                raise

        # Unknown tool
        raise ValueError(f"Unknown tool requested: {tool_name}")

    # Simulate generic tool execution for non-CALL_TOOL plans
    time.sleep(0.2) # Simulate tool execution time
    if "fail" in str(plan).lower():
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
