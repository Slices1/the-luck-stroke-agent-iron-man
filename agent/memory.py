import logging

logger = logging.getLogger(__name__)

class Memory:
    """Minimal agent memory."""
    def __init__(self):
        self.history = []
        logger.debug("Memory initialized.")

    def update(self, input_data, result):
        """Adds a step to the agent's history."""
        step = {"input": input_data, "result": result}
        self.history.append(step)
        logger.debug(f"Memory updated. Total steps: {len(self.history)}")

    def get_history(self):
        """Retrieves the full conversation history."""
        return self.history

    def get_last_n_steps(self, n=5):
        """Retrieves the last N steps."""
        return self.history[-n:]
