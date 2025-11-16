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
    """Standard Agent with dynamic model selection based on prompt difficulty."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        if not STRANDS_AVAILABLE:
            raise ImportError("Strands is not installed. Please install strands package.")

        # Models in decreasing capability order
        self.models = {
            'high': 'anthropic.claude-3-5-sonnet-20240620-v1:0',
            'medium': 'anthropic.claude-3-haiku-20240307-v1:0',
            'low': 'us.amazon.nova-lite-v1:0'
        }

        # Initialize a classifier agent to assess difficulty (using fastest model)
        try:
            self.classifier_agent = Agent(model=self.models['low'])
            self.logger.info(f"Standard Agent initialized with dynamic model selection")
        except Exception as e:
            self.logger.error(f"Failed to initialize classifier agent: {e}")
            raise

    def assess_difficulty(self, user_input):
        """Assess the difficulty of the prompt and return appropriate model."""
        try:
            # Create a prompt to classify difficulty
            classification_prompt = f"""Analyze the following user prompt and classify its difficulty level as either "low", "medium", or "high".

Criteria:
- LOW: Simple questions, basic facts, greetings, straightforward requests (e.g., "What is 2+2?", "Hello", "What's the weather?")
- MEDIUM: Moderately complex tasks requiring some reasoning, explanations, or simple coding (e.g., "Explain how photosynthesis works", "Write a simple function to sort a list")
- HIGH: Complex reasoning, multi-step problems, advanced coding, creative tasks, or nuanced analysis (e.g., "Design a distributed system", "Explain quantum entanglement with mathematical proofs", "Write a complex algorithm")

User prompt: "{user_input}"

Respond with ONLY one word: low, medium, or high."""

            response = self.classifier_agent(classification_prompt)

            # Parse response and extract difficulty
            # Convert AgentResult to string first
            difficulty = str(response).strip().lower()

            # Validate response
            if 'low' in difficulty:
                selected_difficulty = 'low'
            elif 'medium' in difficulty:
                selected_difficulty = 'medium'
            elif 'high' in difficulty:
                selected_difficulty = 'high'
            else:
                # Default to medium if unclear
                self.logger.warning(f"Unclear difficulty classification: {response}. Defaulting to medium.")
                selected_difficulty = 'medium'

            self.logger.info(f"Assessed difficulty: {selected_difficulty} for prompt: {user_input[:50]}...")
            return self.models[selected_difficulty]

        except Exception as e:
            self.logger.error(f"Error assessing difficulty: {e}. Defaulting to medium model.")
            return self.models['medium']

    def run(self, user_input):
        """Process input using dynamically selected model via Strands."""
        try:
            # Assess difficulty and select appropriate model
            selected_model = self.assess_difficulty(user_input)
            self.logger.info(f"Selected model: {selected_model}")

            # Create agent with selected model
            agent = Agent(model=selected_model)

            # Run the actual query
            result = agent(user_input)
            return result

        except Exception as e:
            self.logger.error(f"Standard Agent error: {e}", exc_info=True)
            return f"Error processing request: {e}"


class TaskDecompositionTreeAgent:
    """Agent using Task Decomposition Tree approach."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        if not STRANDS_AVAILABLE:
            raise ImportError("Strands is not installed. Please install strands package.")

        try:
            # Import the orchestrator
            from agent.task_orchestrator import TaskOrchestrator

            self.orchestrator = TaskOrchestrator()
            self.logger.info("Task Decomposition Tree Agent initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize Task Decomposition Tree Agent: {e}")
            raise

    def run(self, user_input):
        """Process input using Task Decomposition Tree."""
        try:
            self.logger.info(f"Processing task with Task Decomposition Tree: {user_input}")

            # Process the task through the three-phase pipeline
            result = self.orchestrator.process_task(user_input)

            # Get tree summary
            summary = self.orchestrator.get_tree_summary()
            self.logger.info(f"Task completed. Tree stats: {summary}")

            return result

        except Exception as e:
            self.logger.error(f"Task Decomposition Tree Agent error: {e}", exc_info=True)
            return f"Error processing request: {e}"


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
