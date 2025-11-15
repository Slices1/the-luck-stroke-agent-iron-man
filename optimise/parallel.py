import logging

logger = logging.getLogger(__name__)

def run_parallel_tasks(tasks: list):
    """
    A stub for parallel execution.
    For the MVP, it just runs tasks sequentially.
    """
    logger.warning("Parallel execution stub: Running tasks sequentially.")
    
    results = []
    for task_function in tasks:
        try:
            results.append(task_function())
        except Exception as e:
            logger.error(f"Task in parallel set failed: {e}")
            results.append(None) # Add None for a failed task
            
    return results
