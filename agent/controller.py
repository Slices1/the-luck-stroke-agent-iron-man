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

        # --- Simple Tool Detection: arithmetic addition ---
        # If user input contains a simple addition expression like "3+4" or "3 + 4",
        # call the add_numbers tool and include the result when calling the LLM.
        import re
        addition_match = re.search(r"(-?\d+(?:\.\d+)?)\s*\+\s*(-?\d+(?:\.\d+)?)", str(input_data))
        augmented_input = input_data
        if addition_match:
            a_str, b_str = addition_match.group(1), addition_match.group(2)
            try:
                sum_val, rep = tools.add_numbers(a_str, b_str)
                self.logger.info(f"Detected addition in input. Computed: {rep}")
                # Append the computed result to the input so the LLM sees it.
                augmented_input = f"{input_data} [computed_addition: {rep}]"
            except Exception:
                self.logger.warning("Addition tool failed; proceeding without computed result.")

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
            # Pass the augmented input (may contain computed results) to reasoning
            plan = reasoning.plan(augmented_input, self.memory, self.model)
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
