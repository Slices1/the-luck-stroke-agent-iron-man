import sys
import os
import logging

# --- CRITICAL IMPORT FIX ---
# This adds the project root to the Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.insert(0, project_root)
# ---------------------------

from agent.controller import AgentController
from utils.logging_utils import setup_logging
from utils.config_loader import load_config
from robustness.chaos_tests import chaos_tool_executor

def main():
    # 1. Setup Logging (Documentation/Demo Team)
    # This loads 'config/logging.yaml' and configures the logger
    setup_logging()
    logger = logging.getLogger("DemoRunner")
    logger.info("Logging configured successfully.")

    # 2. Load Config (All Teams)
    # This loads 'config/settings.yaml'
    config = load_config()
    logger.info(f"Config loaded. Agent timeout set to: {config.get('timeouts', {}).get('step')}")

    # 3. Initialize Agent (Agent-Logic Team)
    agent = AgentController(config)
    logger.info("AgentController initialized.")

    # --- Run 1: Clean Demo Path ---
    logger.info("--- [Running Clean Demo] ---")
    clean_input = "Hello Iron Man track!"
    
    # This input will be caught by the 'fast_path' (Optimisation Team)
    output = agent.run_step(clean_input)
    logger.info(f"Input: '{clean_input}'")
    logger.info(f"Output: '{output}'")
    logger.info("------------------------------\n")

    # --- Run 2: Normal Path (Cache Miss) ---
    logger.info("--- [Running Normal Path (Cache Miss)] ---")
    normal_input = "What is the status of project X?"
    
    # This input will run the full reasoning and tool pipeline
    output = agent.run_step(normal_input)
    logger.info(f"Input: '{normal_input}'")
    logger.info(f"Output: '{output}'")
    logger.info("------------------------------\n")

    # --- Run 3: Cached Path (Cache Hit) ---
    logger.info("--- [Running Normal Path (Cache Hit)] ---")
    
    # This input is identical to Run 2 and should be retrieved from cache
    output = agent.run_step(normal_input)
    logger.info(f"Input: '{normal_input}'")
    logger.info(f"Output: '{output}'")
    logger.info("------------------------------\n")

    # --- Run 4: Chaos/Robustness Test ---
    logger.info("--- [Running Chaos Test (Tool Failure)] ---")
    
    # We replace the agent's tool executor with a 'chaos' one (Robustness Team)
    agent.tool_executor = chaos_tool_executor 
    chaos_input = "This will fail."

    # The agent should catch the failure and return a graceful error (Robustness Team)
    output = agent.run_step(chaos_input)
    logger.info(f"Input: '{chaos_input}'")
    logger.info(f"Output: '{output}'")
    logger.info("------------------------------\n")

    # --- Interactive mode: accept user input and send to the LLM ---
    logger.info("--- [Interactive mode] Type 'quit' or press Enter on empty line to exit ---")
    try:
        while True:
            # Use built-in input() so this works in consoles
            user_input = input("You: ")
            if not user_input or user_input.strip().lower() in ("quit", "exit"):
                logger.info("Exiting interactive mode.")
                break
            # This will cause reasoning.plan to call the model (LLM) and then the tool executor
            output = agent.run_step(user_input)
            print(f"Agent: {output}")
    except (KeyboardInterrupt, EOFError):
        logger.info("Interactive session terminated by user.")

if __name__ == "__main__":
    main()
