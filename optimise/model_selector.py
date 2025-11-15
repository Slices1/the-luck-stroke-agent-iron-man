import logging

logger = logging.getLogger(__name__)

def choose_model(task_type: str = "default"):
    """
    Selects the best model for a given task.
    Iron Man Strategy: Default to fast models.
    """
    if task_type == "complex_reasoning":
        logger.debug("ModelSelector: Choosing powerful model (e.g., gpt-4)")
        return "gpt-4-stub"
    else:
        # Default to a cheap, fast model
        logger.debug("ModelSelector: Choosing fast model (e.g., haiku)")
        return "claude-3-haiku-stub"
