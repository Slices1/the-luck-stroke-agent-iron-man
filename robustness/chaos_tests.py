import random
import time
import logging

logger = logging.getLogger(__name__)

def chaos_tool_executor(plan):
    """
    A replacement for tools.execute_tool that randomly fails or delays
    to test agent robustness.
    """
    roll = random.random() # Random float between 0.0 and 1.0

    if roll < 0.33:
        # --- Test 1: Simulate Latency (Iron Man) ---
        delay = random.uniform(0.5, 1.5) # 500ms - 1500ms delay
        logger.warning(f"[Chaos Test] Injecting {delay:.2f}s delay...")
        time.sleep(delay)
        return f"Delayed chaos response to: {plan}"
    
    elif roll < 0.66:
        # --- Test 2: Simulate Tool Crash (Iron Man) ---
        logger.error("[Chaos Test] Simulating a tool crash!")
        raise ConnectionError("Chaos Test: Tool API connection failed!")

    else:
        # --- Test 3: Simulate Malformed Output (Robustness) ---
        logger.warning("[Chaos Test] Simulating malformed tool output (None)")
        return None # Agent must handle 'None' gracefully
