import random
import time
import logging


# This is your custom API endpoint for the hackathon
STRANDS_ENDPOINT_URL="https://ctwa92wg1b.execute-api.us-east-1.amazonaws.com/prod/invoke"

# These are your credentials from the payload
STRANDS_TEAM_ID="team_the_great_hack_2025_006"
STRANDS_API_TOKEN="qlv4R56nnTH6CJtrUxPRvCBC6D0MIgbRlyFcUKDPbmA"

logger = logging.getLogger(__name__)

logger_start = "[Chaos Test] "

def delay_executor(result:dict):
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

def tool_crush_executor(result:dict):
    roll = random.random()
    if roll < 0.66:
        # --- Test 2: Simulate Tool Crash (Iron Man) ---
        logger.error("[Chaos Test] Simulating a tool crash!")
        raise ConnectionError("Chaos Test: Tool API connection failed!")

def none_result_executor(result:dict):
    roll = random.random()
    if roll < 0.12:
        # --- Test 3: Simulate Malformed Output (Robustness) ---
        logger.warning("[Chaos Test] Simulating malformed tool output (None)")
        return None # Agent must handle 'None' gracefully

def null_result_executor(result:dict) -> dict: # 15% probability to return null content but with normal status
    n = random.randint(1,100)

    new_result = result.copy()

    if (n < 15):
        logger.warning(f"{logger_start}Simulating a null result!")
        new_result["result"] = []
    
    return new_result

def incomplete_result_executor(result:dict) -> dict:
    if not isinstance(result, dict):
        return result

    # 除去 status 的可删除字段列表
    removable_keys = [k for k in result.keys() if k != "status"]

    if len(removable_keys) == 0:
        return result

    # 随机选择一个删除
    key_to_remove = random.choice(removable_keys)

    new_result = result.copy()
    del new_result[key_to_remove]

    return new_result

def partly_null_value_executor(result:dict) -> dict:
    nullifiable_keys = [k for k in result.keys() if k != "status"]
    
    if len(nullifiable_keys) == 0:
        return result
    
    new_result = result.copy()
    new_result[random.choice(nullifiable_keys)] = None

    return new_result



