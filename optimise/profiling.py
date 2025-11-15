import time
import logging

logger = logging.getLogger(__name__)

def time_it(func):
    """Decorator to time a function's execution."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_ms = (end_time - start_time) * 1000
        
        # 'self' (the agent instance) is args[0]
        # 'input_data' is args[1]
        log_message = f"Function '{func.__name__}' took {elapsed_ms:.2f} ms"
        
        # Try to log to the instance's logger if it exists
        if args and hasattr(args[0], 'logger'):
            args[0].logger.info(log_message)
        else:
            logger.info(log_message) # Fallback to module logger
            
        return result
    return wrapper
