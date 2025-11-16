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

class TreeOfThoughtAgent:
    """Tree-of-Thought Agent using Claude Sonnet 3.5 via Strands."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        if not STRANDS_AVAILABLE:
            raise ImportError("Strands is not installed. Please install strands package.")

        try:
            # Initialize Strands agent with Claude Sonnet 3.5
            self.agent = Agent(model="anthropic.claude-3-5-sonnet-20240620-v1:0")
            self.logger.info(f"Tree-of-Thought Agent initialized with Strands Agent (Claude Sonnet 3.5)")
        except Exception as e:
            self.logger.error(f"Failed to initialize Strands Agent: {e}")
            raise

    def run(self, user_input):
        """Process input using Tree-of-Thought approach via Strands."""
        try:
            result = self.agent(user_input)
            return result
        except Exception as e:
            self.logger.error(f"Tree-of-Thought Agent error: {e}", exc_info=True)
            return f"Error processing request: {e}"


class StandardAgent:
    """Standard Agent using Claude Sonnet 3.5 via Strands."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        if not STRANDS_AVAILABLE:
            raise ImportError("Strands is not installed. Please install strands package.")

        try:
            # Initialize Strands agent with Claude Sonnet 3.5
            self.agent = Agent(model="anthropic.claude-3-5-sonnet-20240620-v1:0")
            self.logger.info(f"Standard Agent initialized with Strands Agent (Claude Sonnet 3.5)")
        except Exception as e:
            self.logger.error(f"Failed to initialize Strands Agent: {e}")
            raise

    def run(self, user_input):
        """Process input using standard approach via Strands."""
        try:
            result = self.agent(user_input)
            return result
        except Exception as e:
            self.logger.error(f"Standard Agent error: {e}", exc_info=True)
            return f"Error processing request: {e}"


class TaskDecompositionTreeAgent:
    """Agent using Task Decomposition Tree approach."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Task Decomposition Agent initialized (placeholder)")

    def run(self, user_input):
        """Process input using Task Decomposition Tree (placeholder)."""
        self.logger.warning("Task Decomposition Agent called but not yet implemented")
        return "Task Decomposition Tree Agent is not yet implemented. Please use another agent."


class AgentController:
    def __init__(self, config=None, agent_type='tree-of-thought-agent'):
        """Initialize AgentController with specified agent type.

        Args:
            config: Optional config dict (unused, kept for compatibility)
            agent_type: Type of agent to use ('tree-of-thought-agent', 'standard-agent', 'task-decomposition-tree')
        """
        self.logger = logging.getLogger(__name__)
        self.agent_type = agent_type

        # Initialize the appropriate agent based on type
        if agent_type == 'tree-of-thought-agent':
            self.agent = TreeOfThoughtAgent()
        elif agent_type == 'standard-agent':
            self.agent = StandardAgent()
        elif agent_type == 'task-decomposition-tree':
            self.agent = TaskDecompositionTreeAgent()
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")

        self.logger.info(f"AgentController initialized with agent type: {agent_type}")

    @profiling.time_it
    def run_step(self, input_data):
        """Process input through fast paths or selected agent."""
        self.logger.debug(f"Received input: {input_data}")

        # --- Fast Path Check (agent info & greetings only) ---
        fast_result = fast_paths.fast_path_check(input_data)
        if fast_result:
            self.logger.info("Fast path triggered!")
            return fast_result

        # --- Use Selected Agent ---
        try:
            self.logger.info(f"Using {self.agent_type} agent to process input")
            result = self.agent.run(input_data)
            self.logger.info(f"{self.agent_type} agent returned response")
            return result
        except Exception as e:
            self.logger.error(f"{self.agent_type} agent failed: {e}", exc_info=True)
            return f"I encountered an error processing your request: {e}"
