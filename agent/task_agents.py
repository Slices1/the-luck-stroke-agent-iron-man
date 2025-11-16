"""
Task Agents for the Task Decomposition Tree

This module implements the specialized agents used in the three-phase process:
1. Decomposer: Breaks complex tasks into sub-tasks
2. Verifier: Validates decompositions and identifies leaf nodes
3. Solver: Executes atomic leaf tasks
4. Synthesizer: Combines results from sub-tasks
"""

import logging
import json
from typing import List, Dict, Optional, Any

try:
    from strands import Agent
    STRANDS_AVAILABLE = True
except ImportError:
    STRANDS_AVAILABLE = False


class DecomposerAgent:
    """
    Phase 1: Decomposition Agent

    Breaks down complex tasks into smaller, simpler sub-tasks.
    Uses Claude Haiku for fast, efficient decomposition.
    """

    def __init__(self):
        """Initialize the Decomposer agent."""
        self.logger = logging.getLogger(__name__)

        if not STRANDS_AVAILABLE:
            raise ImportError("Strands is not installed. Please install strands package.")

        # Use Claude Haiku as specified
        self.model = "anthropic.claude-3-haiku-20240307-v1:0"
        self.agent = Agent(model=self.model)
        self.logger.info(f"Decomposer Agent initialized with model: {self.model}")

    def decompose(self, task_description: str) -> List[str]:
        """
        Decompose a task into sub-tasks.

        Args:
            task_description: The task to decompose

        Returns:
            List of sub-task descriptions
        """
        prompt = f"""You are a task decomposition expert. Your job is to break down complex tasks into smaller, logical sub-tasks.

Given the following task:
"{task_description}"

Please decompose this task into 2-5 smaller sub-tasks that:
1. Are logical and necessary steps to complete the main task
2. Can potentially be worked on in parallel (when possible)
3. Are simpler than the original task
4. Together, complete the original task

IMPORTANT: Return ONLY a JSON array of sub-task strings, nothing else.
Format: ["sub-task 1", "sub-task 2", "sub-task 3"]

Example:
Task: "Make breakfast"
Response: ["Make toast", "Make tea"]

Now decompose the given task:"""

        try:
            self.logger.debug(f"Decomposing task: {task_description}")
            response = self.agent(prompt)

            # Parse the JSON response
            # Clean up the response to extract JSON
            # Convert AgentResult to string first
            response_text = str(response).strip()

            # Try to find JSON array in the response
            if '[' in response_text and ']' in response_text:
                start = response_text.index('[')
                end = response_text.rindex(']') + 1
                json_str = response_text[start:end]
                sub_tasks = json.loads(json_str)
            else:
                # Fallback: try parsing the entire response
                sub_tasks = json.loads(response_text)

            if not isinstance(sub_tasks, list):
                raise ValueError("Response is not a list")

            self.logger.info(f"Decomposed into {len(sub_tasks)} sub-tasks")
            return sub_tasks

        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON response: {e}")
            self.logger.error(f"Response was: {response}")
            # Fallback: return a simple decomposition
            return [f"Complete: {task_description}"]
        except Exception as e:
            self.logger.error(f"Error during decomposition: {e}", exc_info=True)
            return [f"Complete: {task_description}"]


class VerifierAgent:
    """
    Phase 2: Verification Agent

    Verifies decompositions and identifies leaf nodes (atomic tasks).
    Acts as a peer reviewer to ensure quality.
    """

    def __init__(self):
        """Initialize the Verifier agent."""
        self.logger = logging.getLogger(__name__)

        if not STRANDS_AVAILABLE:
            raise ImportError("Strands is not installed. Please install strands package.")

        # Use Claude Haiku for fast verification
        self.model = "anthropic.claude-3-haiku-20240307-v1:0"
        self.agent = Agent(model=self.model)
        self.logger.info(f"Verifier Agent initialized with model: {self.model}")

    def is_leaf_node(self, task_description: str, parent_task: Optional[str] = None) -> bool:
        """
        Determine if a task is a leaf node (atomic, one-shot executable).

        Args:
            task_description: The task to verify
            parent_task: Optional parent task for context

        Returns:
            True if the task is a leaf node, False otherwise
        """
        context = f"\nParent task: {parent_task}" if parent_task else ""

        prompt = f"""You are a task verification expert. Your job is to determine if a task is "atomic" (simple enough to be executed in one step by a simple AI model).

Task: "{task_description}"{context}

A task is a LEAF NODE (atomic) if:
1. It is simple and well-defined
2. It can be completed in a single step
3. It does NOT require breaking down into sub-steps
4. A simple AI model could answer/execute it reliably

Examples of LEAF NODES:
- "What is 2+2?"
- "Get bread from pantry"
- "Boil water"
- "Define what photosynthesis means"
- "Turn on the toaster"

Examples of NON-LEAF NODES (need decomposition):
- "Make breakfast" (needs: make toast, make tea, etc.)
- "Explain quantum physics" (needs: multiple concepts explained)
- "Build a web application" (needs: many sub-tasks)

Is this task a leaf node?
Respond with ONLY one word: YES or NO"""

        try:
            self.logger.debug(f"Verifying if leaf node: {task_description}")
            response = self.agent(prompt)

            # Parse response
            # Convert AgentResult to string first
            response_text = str(response).strip().upper()
            is_leaf = 'YES' in response_text

            self.logger.info(f"Task '{task_description}' is leaf: {is_leaf}")
            return is_leaf

        except Exception as e:
            self.logger.error(f"Error during verification: {e}", exc_info=True)
            # Default to considering it a leaf to avoid infinite decomposition
            return True

    def verify_decomposition(self, parent_task: str, sub_tasks: List[str]) -> bool:
        """
        Verify if a decomposition is logical and complete.

        Args:
            parent_task: The original task
            sub_tasks: The proposed sub-tasks

        Returns:
            True if decomposition is valid, False otherwise
        """
        prompt = f"""You are a task verification expert. Evaluate if the following task decomposition is logical and complete.

Parent Task: "{parent_task}"

Sub-tasks:
{chr(10).join(f'{i+1}. {task}' for i, task in enumerate(sub_tasks))}

Is this a good decomposition? Check if:
1. The sub-tasks are logical steps toward completing the parent task
2. Together, the sub-tasks would complete the parent task
3. The sub-tasks are simpler than the parent task

Respond with ONLY one word: YES or NO"""

        try:
            self.logger.debug(f"Verifying decomposition of: {parent_task}")
            response = self.agent(prompt)

            # Parse response
            # Convert AgentResult to string first
            response_text = str(response).strip().upper()
            is_valid = 'YES' in response_text

            self.logger.info(f"Decomposition valid: {is_valid}")
            return is_valid

        except Exception as e:
            self.logger.error(f"Error during decomposition verification: {e}", exc_info=True)
            # Default to accepting the decomposition
            return True


class SolverAgent:
    """
    Solver Agent for Leaf Nodes

    Executes atomic tasks using a small, efficient model.
    Used in Phase 3 to execute leaf nodes.
    """

    def __init__(self):
        """Initialize the Solver agent."""
        self.logger = logging.getLogger(__name__)

        if not STRANDS_AVAILABLE:
            raise ImportError("Strands is not installed. Please install strands package.")

        # Use Amazon Nova Lite for fast, efficient execution
        self.model = "us.amazon.nova-lite-v1:0"
        self.agent = Agent(model=self.model)
        self.logger.info(f"Solver Agent initialized with model: {self.model}")

    def solve(self, task_description: str) -> str:
        """
        Execute an atomic task and return the result.

        Args:
            task_description: The task to execute

        Returns:
            The result/answer for the task
        """
        prompt = f"""You are a helpful assistant. Please complete the following task or answer the following question:

{task_description}

Provide a clear, concise answer or solution."""

        try:
            self.logger.debug(f"Solving task: {task_description}")
            response = self.agent(prompt)
            self.logger.info(f"Task solved successfully")
            # Convert AgentResult to string first
            return str(response).strip()

        except Exception as e:
            self.logger.error(f"Error during task execution: {e}", exc_info=True)
            return f"Error executing task: {str(e)}"


class SynthesizerAgent:
    """
    Phase 3: Synthesizer Agent

    Combines results from sub-tasks to create solutions for parent tasks.
    Works bottom-up, merging solutions like a merge sort.
    """

    def __init__(self):
        """Initialize the Synthesizer agent."""
        self.logger = logging.getLogger(__name__)

        if not STRANDS_AVAILABLE:
            raise ImportError("Strands is not installed. Please install strands package.")

        # Use Amazon Nova Lite as specified
        self.model = "us.amazon.nova-lite-v1:0"
        self.agent = Agent(model=self.model)
        self.logger.info(f"Synthesizer Agent initialized with model: {self.model}")

    def synthesize(self, parent_task: str, sub_results: List[Dict[str, str]]) -> str:
        """
        Combine results from sub-tasks into a solution for the parent task.

        Args:
            parent_task: The parent task description
            sub_results: List of dicts with 'task' and 'result' keys

        Returns:
            Combined result for the parent task
        """
        # Format the sub-results
        results_text = "\n\n".join(
            f"Sub-task: {item['task']}\nResult: {item['result']}"
            for item in sub_results
        )

        prompt = f"""You are a synthesis expert. Your job is to combine results from sub-tasks into a complete answer for the parent task.

Parent Task: "{parent_task}"

Sub-task Results:
{results_text}

Please synthesize these results into a coherent, complete answer for the parent task.
The answer should:
1. Address the parent task directly
2. Integrate information from all sub-tasks
3. Be clear and well-organized
4. Flow naturally as a unified response"""

        try:
            self.logger.debug(f"Synthesizing results for: {parent_task}")
            response = self.agent(prompt)
            self.logger.info(f"Synthesis completed successfully")
            # Convert AgentResult to string first
            return str(response).strip()

        except Exception as e:
            self.logger.error(f"Error during synthesis: {e}", exc_info=True)
            # Fallback: concatenate results
            fallback = f"Results for: {parent_task}\n\n"
            fallback += "\n\n".join(f"- {item['result']}" for item in sub_results)
            return fallback
