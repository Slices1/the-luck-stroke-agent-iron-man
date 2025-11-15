import logging
from agent import reasoning, memory, tools
from optimise import caching, model_selector, fast_paths, profiling
from robustness import error_handlers, validators

class AgentController:
    def __init__(self, config):
        self.memory = memory.Memory()
        self.model = tools.LLMModel() # Using the stub model from tools for now
        self.config = config
        self.logger = logging.getLogger(__name__) # Gets the logger configured in run_demo
        self.tool_executor = tools.execute_tool # Default, can be swapped for testing

        # Team roles can see their modules being used
        self.logger.info("AgentController initialized with modules:")
        self.logger.info("- Caching (Optimise)")
        self.logger.info("- Fast Paths (Optimise)")
        self.logger.info("- Validators (Robustness)")
        self.logger.info("- Error Handlers (Robustness)")

    @profiling.time_it # Decorator from Optimisation Team
    def run_step(self, input_data):
        self.logger.debug(f"Received new step with input: {input_data}")

        # Note: tool selection and calls are delegated to the LLM's plan.
        # The LLM (or its placeholder) will return a plan indicating whether to
        # call a tool (e.g. "CALL_TOOL:add_numbers:2+3+4"). We intentionally do
        # not pre-run arithmetic tools here so the LLM can decide when to call
        # them. This makes it easy to replace the placeholder LLM later.

        # --- Optimisation Team: Fast Path Check ---
        fast_result = fast_paths.fast_path_check(input_data)
        if fast_result:
            self.logger.info("Fast path triggered!")
            return fast_result

        # --- Robustness Team: Input Validation ---
        if not validators.validate_input(input_data):
            self.logger.warning(f"Invalid input detected: {input_data}")
            return error_handlers.handle_invalid_input(input_data)

        # --- Optimisation Team: Cache Check ---
        cached_result = caching.get_cached_response(input_data)
        if cached_result:
            self.logger.info("Cache hit!")
            return cached_result
        
        self.logger.info("Cache miss, proceeding with full pipeline.")

        # --- Agent-Logic Team: Core Loop ---
        try:
            # 1. Select Model (Optimisation Team)
            model_name = model_selector.choose_model(task_type="default")
            self.logger.debug(f"Model selected: {model_name}")

            # 2. Reason (Agent-Logic Team)
            # Pass the raw user input to reasoning; the LLM placeholder may
            # return a plan that instructs a tool call (CALL_TOOL:...)
            plan = reasoning.plan(input_data, self.memory, self.model)
            self.logger.debug(f"Plan generated: {plan}")

            # 3. Execute Tool (Agent-Logic + Robustness Team)
            # We wrap this in a try/except to test robustness
            tool_result = self.tool_executor(plan)
            self.logger.debug(f"Tool executed, result: {tool_result}")

        except Exception as e:
            # --- Robustness Team: Error Handling ---
            self.logger.error(f"An error occurred during agent step: {e}", exc_info=True)
            return error_handlers.handle_tool_failure(e, plan)

        # --- Agent-Logic Team: Memory Update ---
        self.memory.update(input_data, tool_result)

        # --- Optimisation Team: Cache Update ---
        caching.set_cached_response(input_data, tool_result)

        return tool_result
