import sys
import os
import logging

# --- CRITICAL IMPORT FIX ---
# This adds the project root (the directory this file is in) to the Python path
# This allows us to import 'agent', 'utils', etc.
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)
# ---------------------------

from agent.controller import AgentController
from utils.logging_utils import setup_logging
from utils.config_loader import load_config

def main():
    # 1. Setup Logging
    # This loads 'config/logging.yaml' and configures the logger
    setup_logging()
    # We use a specific logger name so it's clear in the logs
    logger = logging.getLogger("ChatInterface")
    logger.info("Logging configured successfully.")

    # 2. Load Config
    # This loads 'config/settings.yaml'
    config = load_config()
    logger.info(f"Config loaded. Agent timeout set to: {config.get('timeouts', {}).get('step')}")

    # 3. Initialize Agent (Agent-Logic Team)
    agent = AgentController(config)
    logger.info("AgentController initialized. Ready for conversation.")

    # 4. Start Interactive Chat Loop
    print("\n--- Iron Man Agent Chat ---")
    print("Agent: Hello! I'm the Iron Man Agent. How can I help you?")
    print("       (Type 'exit' or 'quit' to end the conversation.)")
    print("-" * 30)

    while True:
        try:
            # Get user input from the console
            user_input = input("You: ")    
            
            # Open a banner for the logs
            print("-"*13 + " Logs " + "-"*12)

            
            # Check for exit commands
            if user_input.lower() in ['exit', 'quit']:
                print("Agent: Goodbye!")
                logger.info("Chat session ended by user.")
                break  # Exit the while loop

            # Send the input to the agent and get the response
            logger.info(f"Input: '{user_input}'")
            agent_response = agent.run_step(user_input)
            
            # Print the agent's response to the console
            logger.info(f"Output: '{agent_response}'")

            # Close the banner for the logs
            print("-"*30 + "\n\n")

            print(f"Agent: {agent_response}\n")


        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\nAgent: Conversation interrupted. Goodbye!")
            logger.info("Chat session interrupted (KeyboardInterrupt).")
            break
        except Exception as e:
            # Handle any unexpected error during agent.run_step()
            logger.error(f"An unexpected error occurred: {e}", exc_info=True)
            print(f"Agent: I'm sorry, an internal error occurred. Please try your request again.")

if __name__ == "__main__":
    main()
