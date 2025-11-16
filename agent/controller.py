import logging
import os
from dotenv import load_dotenv
from optimise import fast_paths, profiling

# Load environment variables for Strands agent
load_dotenv()

# Try to import Strands components
try:
    from strands import Agent
    from strands_tools import calculator, speak, use_computer
    STRANDS_AVAILABLE = True
except ImportError:
    STRANDS_AVAILABLE = False

class AgentController:
    def __init__(self, config=None):
        """Initialize AgentController with Strands Agent.

        Args:
            config: Optional config dict (unused, kept for compatibility with chat.py)
        """
        self.logger = logging.getLogger(__name__)

        # Initialize Strands agent
        self.strands_agent = None

        if STRANDS_AVAILABLE:
            try:
                # Initialize Strands agent with tools
                self.strands_agent = Agent(tools=[calculator, speak, use_computer])
                self.logger.info("Strands Agent initialized with tools: calculator, speak, use_computer")
            except Exception as e:
                self.logger.error(f"Failed to initialize Strands Agent: {e}")
                print(f"Strands init error: {e}")
        else:
            self.logger.error("Strands is not installed. Please install strands and strands_tools.")

        self.logger.info("AgentController initialized with Strands Agent")

    @profiling.time_it
    def run_step(self, input_data):
        """Process input through fast paths or Strands agent."""
        self.logger.debug(f"Received input: {input_data}")

        # --- Fast Path Check (agent info & greetings only) ---
        fast_result = fast_paths.fast_path_check(input_data)
        if fast_result:
            self.logger.info("Fast path triggered!")
            return fast_result

        # --- Use Strands Agent ---
        if self.strands_agent:
            try:
                self.logger.info("Using Strands Agent to process input")
                result = self.strands_agent(input_data)
                self.logger.info(f"Strands Agent returned: {result}")
                return result
            except Exception as e:
                self.logger.error(f"Strands Agent failed: {e}", exc_info=True)
                print(f"DEBUG: Strands Agent Error: {e}")
                import traceback
                traceback.print_exc()
                return "I encountered an error processing your request. Please try again."
        else:
            self.logger.error("Strands Agent not available")
            return "Strands Agent is not properly initialized."
