import logging
import os

logger = logging.getLogger(__name__)


def choose_model(task_type: str = "default"):
    """
    Selects the best model for a given task.
    Behavior:
    - If an environment override `CHAT_SELECTED_MODEL` is set, return it (used by `chat.py`).
    - Otherwise, normalize `task_type` and choose a model name string.

    This function returns a string identifier (e.g., "gpt-4-stub") which other
    parts of the system can interpret.
    """
    # 1) Honor explicit environment override set by the chat UI (chat.py)
    env_override = os.getenv("CHAT_SELECTED_MODEL")
    if env_override:
        logger.debug(f"ModelSelector: Using env override model '{env_override}'")
        return env_override

    # 2) Normalize the task_type for matching
    t = (task_type or "").strip().lower()

    if t in ("implementation 1", "1", "one", "gpt4", "gpt-4"):
        logger.debug("ModelSelector: Switches between bigger and smaller model depending on user query.")
        return "gpt-4-stub"
    elif t in ("implementation 2", "2", "two", "fast", "cheap"):
        logger.debug("ModelSelector: Using fast/cheap model (haiku stub)")
        return "claude-3-haiku-stub"
    elif t in ("implementation 3", "3", "three", "balanced"):
        logger.debug("ModelSelector: Hierarchical/balanced model selection")
        return "gpt-3.5-turbo-stub"
    # Interactive switch: allow user to change module at runtime
    if t in ("switch module", "switch agent", "switch"):
        # Provide a simple interactive selection prompt. Keep looping until
        # a valid choice is made or the user cancels with 'q'.
        prompt = (
            "Select a module to switch to:\n"
            "  1) Agent 1 (gpt-4-stub)\n"
            "  2) Agent 2 (claude-3-haiku-stub)\n"
            "  3) Agent 3 (gpt-3.5-turbo-stub)\n"
            "Enter 1/2/3 (or 'q' to cancel): "
        )
        while True:
            try:
                choice = input(prompt).strip().lower()
            except (EOFError, KeyboardInterrupt):
                # If input is not available or user interrupts, cancel gracefully
                logger.info("ModelSelector: switch cancelled by user (no input).")
                return "claude-3-haiku-stub"

            if choice in ("q", "quit", "cancel"):
                logger.info("ModelSelector: switch cancelled by user.")
                print("Switch cancelled.")
                return "claude-3-haiku-stub"
            if choice in ("1", "one"):
                print("Switched to Agent 1 (gpt-4-stub)")
                logger.info("ModelSelector: Switched to Agent 1 via interactive prompt.")
                return "gpt-4-stub"
            if choice in ("2", "two"):
                print("Switched to Agent 2 (claude-3-haiku-stub)")
                logger.info("ModelSelector: Switched to Agent 2 via interactive prompt.")
                return "claude-3-haiku-stub"
            if choice in ("3", "three"):
                print("Switched to Agent 3 (gpt-3.5-turbo-stub)")
                logger.info("ModelSelector: Switched to Agent 3 via interactive prompt.")
                return "gpt-3.5-turbo-stub"

            print("Invalid selection. Please enter 1, 2, 3, or 'q' to cancel.")
    else:
        logger.debug("ModelSelector: Choosing default fast model (haiku)")
        return "claude-3-haiku-stub"


''' if user_input.lower() in ['switch agent']:
                print("Select an agent to switch to (1, 2, 3): ")
                if user_input.lower() in ['1', 'one']:
                    print("Agent 1 is chosen. Enter your query:")
                    # Get user input from the console
                    user_input = input("You: ")    
                    # Open a banner for the logs
                    print("-"*13 + " Logs " + "-"*12)
                    break  # Exit the while loop
                if user_input.lower() in ['2', 'two']:
                    print("Agent 2 is chosen. Enter your query:")
                    # Get user input from the console
                    user_input = input("You: ")    
                    # Open a banner for the logs
                    print("-"*13 + " Logs " + "-"*12)
                    break  # Exit the while loop
                if user_input.lower() in ['3', 'three']:
                    print("Agent 3 is chosen. Enter your query:")
                    # Get user input from the console
                    user_input = input("You: ")    
                    # Open a banner for the logs
                    print("-"*13 + " Logs " + "-"*12)
                    break  # Exit the while loop
                break  # Exit the while loop'''
