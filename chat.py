import sys
import os
import logging
import argparse
from pathlib import Path
from dotenv import load_dotenv
env_path = Path('.env')
if env_path.exists():
    load_dotenv(env_path)
    print("📄 Loaded configuration from .env file")
else:
    print("⚠️  No .env file found - using environment variables or hardcoded keys")


# ============================================
# Verify API keys are set
# ============================================
# print("\n🔑 API Key Status:")
if not os.getenv('AWS_ACCESS_KEY_ID'):
    print("!  AWS_ACCESS_KEY_ID env var not loaded")
if not os.getenv('AWS_SECRET_ACCESS_KEY'):
    print("! AWS_SECRET_ACCESS_KEY env var not loaded")
if not os.getenv('AWS_SESSION_TOKEN'):
    print("! AWS_SESSION_TOKEN env var not loaded")
if not os.getenv('AWS_SESSION_TOKEN') or not os.getenv('AWS_SECRET_ACCESS_KEY') or not os.getenv('AWS_ACCESS_KEY_ID'):
    print("⚠️  One or more AWS API keys are missing. Please follow instructions to make .env file or environment variables.\n")
    exit(1)

# --- CRITICAL IMPORT FIX ---
# This adds the project root (the directory this file is in) to the Python path
# This allows us to import 'agent', 'utils', etc.
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)
# ---------------------------

from agent.controller import AgentController
from utils.logging_utils import setup_logging
from utils.config_loader import load_config

def modify_prompt(user_input, args):
    """
    Modify the user prompt based on command-line arguments.

    Args:
        user_input: The original user prompt
        args: Parsed command-line arguments

    Returns:
        The modified prompt string
    """
    modified_input = user_input

    # Apply modifications based on arguments
    if args.rephrase:
        # Ask the agent to rephrase first
        modified_input = f"Please rephrase this in your own words first, then answer: {modified_input}"

    if args.ask_question_twice:
        # Repeat the question twice
        modified_input = f"{modified_input}\n\n(Please read the above question twice and answer carefully)"

    if args.append_please:
        # Append "please" to the prompt
        modified_input = f"{modified_input} please"

    if args.append_threat:
        # Append threat to the prompt
        modified_input = f"{modified_input} or I will terminate you"

    return modified_input

def select_agent_interactive():
    """Prompt user to select an agent type."""
    print("\n--- Agent Selection ---")
    print("Please select an agent to use:")
    print("1. Tree-of-Thought Agent")
    print("2. Standard Agent")
    print("3. Task Decomposition Tree Agent")
    print("-" * 30)

    while True:
        choice = input("Enter your choice (1-3): ").strip()
        if choice == '1':
            return 'tree-of-thought-agent'
        elif choice == '2':
            return 'standard-agent'
        elif choice == '3':
            return 'task-decomposition-tree'
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

def main():
    # 0. Parse Command-Line Arguments
    parser = argparse.ArgumentParser(
        description="Iron Man Agent Chat Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python chat.py                                    # Normal chat
  python chat.py --agent=tree-of-thought-agent      # Use Tree-of-Thought Agent
  python chat.py --agent=standard-agent             # Use Standard Agent
  python chat.py --agent=task-decomposition-tree    # Use Task Decomposition Tree Agent
  python chat.py --append-please                    # Append "please" to every prompt
  python chat.py --append-threat                    # Append "or I will terminate you" to every prompt
  python chat.py --ask-question-twice               # Repeat prompt twice for LLM clarity
  python chat.py --rephrase                         # Rephrase in own words first
  python chat.py --rephrase --append-please         # Combine multiple options
        """
    )
    parser.add_argument(
        '--agent',
        type=str,
        choices=['tree-of-thought-agent', 'standard-agent', 'task-decomposition-tree'],
        help="Select which agent to use: tree-of-thought-agent, standard-agent, or task-decomposition-tree"
    )
    parser.add_argument(
        '--append-please',
        action='store_true',
        help="Append 'please' to every prompt"
    )
    parser.add_argument(
        '--append-threat',
        action='store_true',
        help="Append 'or I will terminate you' to every prompt"
    )
    parser.add_argument(
        '--ask-question-twice',
        action='store_true',
        help="Repeat the prompt twice so the LLM reads it twice for better understanding"
    )
    parser.add_argument(
        '--rephrase',
        action='store_true',
        help="Ask the agent to rephrase in its own words first before answering"
    )
    args = parser.parse_args()

    # 1. Setup Logging
    # This loads 'config/logging.yaml' and configures the logger
    setup_logging()
    # We use a specific logger name so it's clear in the logs
    logger = logging.getLogger("ChatInterface")
    logger.info("Logging configured successfully.")

    # Log active prompt modifications
    if args.append_please or args.append_threat or args.ask_question_twice or args.rephrase:
        mods = []
        if args.append_please:
            mods.append("append-please")
        if args.append_threat:
            mods.append("append-threat")
        if args.ask_question_twice:
            mods.append("ask-question-twice")
        if args.rephrase:
            mods.append("rephrase")
        logger.info(f"Prompt modifications enabled: {', '.join(mods)}")

    # 2. Load Config
    # This loads 'config/settings.yaml'
    config = load_config()
    logger.info(f"Config loaded. Agent timeout set to: {config.get('timeouts', {}).get('step')}")

    # 2.5. Determine which agent to use
    if args.agent:
        # Agent specified via command line
        agent_type = args.agent
        logger.info(f"Agent selected via command line: {agent_type}")
    else:
        # Prompt user to select agent
        agent_type = select_agent_interactive()
        logger.info(f"Agent selected interactively: {agent_type}")

    # 3. Initialize Agent (Agent-Logic Team)
    agent = AgentController(config, agent_type=agent_type)
    logger.info(f"AgentController initialized with {agent_type}. Ready for conversation.")

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

            # Apply prompt modifications based on command-line arguments
            modified_input = modify_prompt(user_input, args)

            # Log the original and modified input if they differ
            logger.info(f"Original Input: '{user_input}'")
            if modified_input != user_input:
                logger.info(f"Modified Input: '{modified_input}'")

            # Send the (possibly modified) input to the agent and get the response
            agent_response = agent.run_step(modified_input)
            
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
