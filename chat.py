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
from optimise.model_selector import choose_model

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
    controller = AgentController(config)
    logger.info("AgentController initialized. Ready for conversation.")

    # 4. Start Interactive Chat Loop
    print("\n--- Iron Man Agent Chat ---")
    print("Agent: Hello! I'm the Iron Man Agent. How can I help you?")
    print("       (Type 'exit' or 'quit' to end the conversation.)")
    print("-" * 30)

    while True:
        try:
            # Get user input from the console
            user_input = input("You: ").strip()
            
            # Open a banner for the logs
            print("-"*13 + " Logs " + "-"*12)

            
            # Check for exit commands
            if user_input.lower() in ['exit', 'quit']:
                print("Agent: Goodbye!")
                logger.info("Chat session ended by user.")
                break  # Exit the while loop

            

            # Decide which model/implementation to use for this input
            selected_model = choose_model(user_input)
            # Expose this choice to other modules (AgentController calls choose_model internally)
            # We set an env var so the optimiser's chooser can pick up the user's selection
            import os
            os.environ["CHAT_SELECTED_MODEL"] = selected_model

            logger.info(f"Input: '{user_input}' (task_type -> selected model: {selected_model})")
            # Send the input to the agent controller pipeline and get the response
            agent_response = controller.run_step(user_input)
            
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
