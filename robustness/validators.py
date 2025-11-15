import logging

logger = logging.getLogger(__name__)
MAX_INPUT_LENGTH = 1024 # Example constraint

def validate_input(input_data: str):
    """
    Checks if the input is valid.
    Returns True if valid, False otherwise.
    """
    if not input_data:
        logger.warning("Validation failed: Input is empty.")
        return False
        
    if not isinstance(input_data, str):
        logger.warning("Validation failed: Input is not a string.")
        return False
        
    if len(input_data) > MAX_INPUT_LENGTH:
        logger.warning(f"Validation failed: Input exceeds {MAX_INPUT_LENGTH} chars.")
        return False
        
    logger.debug("Validation successful.")
    return True
