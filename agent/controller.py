import logging
from agent import memory, tools
from optimise import caching, model_selector, fast_paths, profiling
from robustness import error_handlers, validators

class AgentController:
    def __init__(self, config):
        self.memory = memory.Memory()
        # Initialize preferred model: Strands Agent (with OpenAIModel) if
        # available, otherwise the local LLMModel stub.
        self.model = tools.get_preferred_model(config)
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

        # No pre-run tools: the Agent (LLM) is asked first and may decide to use
        # tools. Per your request, we initialize and use the Strands Agent (if
        # available) before any tool execution.

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

            # 2. Ask the Agent (LLM) directly with the user input. The Agent is
            # expected to produce a direct answer or a plan; tools are not run
            # here unless the Agent explicitly requests them and the pipeline
            # is extended to support that.
            try:
                model_response = self.model.query(input_data)
            except Exception as e_model:
                self.logger.error(f"LLM/model query failed: {e_model}", exc_info=True)
                return error_handlers.handle_tool_failure(e_model, None)

            tool_result = model_response
            self.logger.debug(f"Model returned: {tool_result}")

        except Exception as e:
            # --- Robustness Team: Error Handling ---
            self.logger.error(f"An error occurred during agent step: {e}", exc_info=True)
            return error_handlers.handle_tool_failure(e, None)

        # --- Agent-Logic Team: Memory Update ---
        self.memory.update(input_data, tool_result)

        # --- Optimisation Team: Cache Update ---
        caching.set_cached_response(input_data, tool_result)

        return tool_result
