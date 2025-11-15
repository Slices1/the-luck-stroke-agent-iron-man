import time
import logging

class Timer:
    """A simple context manager for timing blocks of code."""
    def __init__(self, logger, name: str = "operation"):
        self.name = name
        self.logger = logger
        self._start_time = None

    def __enter__(self):
        self._start_time = time.perf_counter()
        self.logger.debug(f"[Timer] Starting '{self.name}'...")

    def __exit__(self, exc_type, exc_value, traceback):
        elapsed_ms = (time.perf_counter() - self._start_time) * 1000
        self.logger.info(f"[Timer] Finished '{self.name}' in {elapsed_ms:.2f} ms")
