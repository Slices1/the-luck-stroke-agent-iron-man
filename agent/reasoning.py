import logging

logger = logging.getLogger(__name__)

def plan(input_data, memory, model):
    """
    Minimal reasoning stub.
    Generates a 'plan' to be executed by a tool.
    """
    # Prefer asking the provided model for a plan if it supports `query()`.
    # This lets the agent send the user's input to the LLM and use the
    # model's response as the execution plan.
    try:
        prompt = (
            f"Create an execution plan for the following input:\n" \
            f"Input: {input_data}\n\n" \
            f"Recent memory (last 5 steps): {memory.get_last_n_steps(5)}\n" \
            "Provide a short plan the tool executor can follow."
        )
        # model.query may raise if model is a stub or unavailable
        llm_response = model.query(prompt)
        logger.debug(f"LLM returned plan: {llm_response}")
        return llm_response
    except Exception as e:
        logger.warning(f"LLM plan generation failed, falling back to simple plan: {e}")
        # Fallback MVP Plan: create a simple instruction string
        plan_steps = f"Call a tool to process the input: '{input_data}'"
        logger.debug(f"Generated fallback plan: {plan_steps}")
        return plan_steps
