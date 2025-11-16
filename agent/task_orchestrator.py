"""
Task Decomposition Tree Orchestrator

This module orchestrates the three-phase process:
1. Phase 1: Decomposition (Top-Down)
2. Phase 2: Verification (Peer Review)
3. Phase 3: Synthesis (Bottom-Up)
"""

import logging
from typing import List, Dict, Optional, Any
from agent.task_tree import TaskDecompositionTree, TaskNode, TaskStatus
from agent.task_agents import DecomposerAgent, VerifierAgent, SolverAgent, SynthesizerAgent


class TaskOrchestrator:
    """
    Orchestrates the complete Task Decomposition Tree process.

    Manages the three phases:
    1. Build the tree through recursive decomposition and verification
    2. Execute all leaf nodes
    3. Synthesize results bottom-up to get the final answer
    """

    def __init__(self):
        """Initialize the orchestrator with all required agents."""
        self.logger = logging.getLogger(__name__)

        # Initialize all agents
        try:
            self.decomposer = DecomposerAgent()
            self.verifier = VerifierAgent()
            self.solver = SolverAgent()
            self.synthesizer = SynthesizerAgent()
            self.logger.info("Task Orchestrator initialized with all agents")
        except Exception as e:
            self.logger.error(f"Failed to initialize agents: {e}")
            raise

        self.tree: Optional[TaskDecompositionTree] = None
        self.max_depth = 5  # Prevent infinite recursion

    def process_task(self, task_description: str) -> str:
        """
        Process a task through the complete three-phase pipeline.

        Args:
            task_description: The task to process

        Returns:
            The final result after synthesis
        """
        self.logger.info(f"Starting task processing: {task_description}")

        try:
            # Initialize the tree
            self.tree = TaskDecompositionTree(task_description)

            # Phase 1 & 2: Build the tree (decomposition + verification)
            self.logger.info("=== Phase 1 & 2: Decomposition and Verification ===")
            self._build_tree()

            # Log the tree structure
            self.logger.info("Task tree built successfully:")
            self.tree.print_tree()

            # Phase 3: Execute and synthesize
            self.logger.info("=== Phase 3: Execution and Synthesis ===")
            result = self._execute_and_synthesize()

            self.logger.info("Task processing completed successfully")
            return result

        except Exception as e:
            self.logger.error(f"Error processing task: {e}", exc_info=True)
            return f"Error processing task: {str(e)}"

    def _build_tree(self):
        """
        Build the task tree through recursive decomposition and verification.

        This combines Phase 1 (Decomposition) and Phase 2 (Verification).
        """
        # Start with root node
        self._decompose_node(self.tree.root, depth=0)

    def _decompose_node(self, node: TaskNode, depth: int):
        """
        Recursively decompose a node until all branches end in leaf nodes.

        Args:
            node: The node to decompose
            depth: Current depth in the tree (for max depth check)
        """
        # Check max depth to prevent infinite recursion
        if depth >= self.max_depth:
            self.logger.warning(f"Max depth {self.max_depth} reached for node {node.node_id}. Marking as leaf.")
            node.mark_as_leaf()
            node.status = TaskStatus.VERIFIED
            return

        self.logger.debug(f"Processing node at depth {depth}: {node.task_description}")

        # Phase 2: Check if this is a leaf node
        parent_task = None
        if node.parent_id and node.parent_id in self.tree.nodes:
            parent_task = self.tree.nodes[node.parent_id].task_description

        is_leaf = self.verifier.is_leaf_node(node.task_description, parent_task)

        if is_leaf:
            # This is a leaf node - no further decomposition needed
            node.mark_as_leaf()
            node.status = TaskStatus.VERIFIED
            self.logger.info(f"Node {node.node_id} verified as leaf")
            return

        # Phase 1: Decompose the task
        node.status = TaskStatus.DECOMPOSING
        sub_tasks = self.decomposer.decompose(node.task_description)

        if not sub_tasks or len(sub_tasks) == 0:
            # Decomposition failed or returned empty - mark as leaf
            self.logger.warning(f"Decomposition returned no sub-tasks for {node.node_id}. Marking as leaf.")
            node.mark_as_leaf()
            node.status = TaskStatus.VERIFIED
            return

        # Verify the decomposition quality
        is_valid = self.verifier.verify_decomposition(node.task_description, sub_tasks)

        if not is_valid:
            # Decomposition not valid - mark as leaf and let solver handle it
            self.logger.warning(f"Decomposition not valid for {node.node_id}. Marking as leaf.")
            node.mark_as_leaf()
            node.status = TaskStatus.VERIFIED
            return

        # Add sub-tasks as children
        for sub_task in sub_tasks:
            child_node = self.tree.add_node(sub_task, node.node_id)
            # Recursively decompose each child
            self._decompose_node(child_node, depth + 1)

        # Mark this node as verified (not a leaf, but properly decomposed)
        node.status = TaskStatus.VERIFIED
        self.logger.info(f"Node {node.node_id} decomposed into {len(sub_tasks)} sub-tasks")

    def _execute_and_synthesize(self) -> str:
        """
        Execute leaf nodes and synthesize results bottom-up.

        Returns:
            The final synthesized result for the root task
        """
        # Execute all leaf nodes
        self._execute_leaves()

        # Synthesize results bottom-up
        return self._synthesize_node(self.tree.root)

    def _execute_leaves(self):
        """Execute all leaf nodes in the tree."""
        leaf_nodes = self.tree.get_leaf_nodes()
        self.logger.info(f"Executing {len(leaf_nodes)} leaf nodes")

        for leaf in leaf_nodes:
            try:
                leaf.status = TaskStatus.EXECUTING
                self.logger.debug(f"Executing leaf {leaf.node_id}: {leaf.task_description}")

                # Execute the task
                result = self.solver.solve(leaf.task_description)

                # Store the result
                leaf.set_result(result)
                self.logger.info(f"Leaf {leaf.node_id} executed successfully")

            except Exception as e:
                self.logger.error(f"Error executing leaf {leaf.node_id}: {e}")
                leaf.set_error(str(e))

    def _synthesize_node(self, node: TaskNode) -> str:
        """
        Synthesize results for a node from its children (bottom-up).

        Args:
            node: The node to synthesize

        Returns:
            The synthesized result for this node
        """
        # Base case: leaf node - return its result
        if node.is_leaf:
            if node.result:
                return node.result
            elif node.error:
                return f"Error: {node.error}"
            else:
                # Fallback: execute the leaf if not already done
                self.logger.warning(f"Leaf node {node.node_id} has no result. Executing now.")
                try:
                    result = self.solver.solve(node.task_description)
                    node.set_result(result)
                    return result
                except Exception as e:
                    error = str(e)
                    node.set_error(error)
                    return f"Error: {error}"

        # Recursive case: synthesize from children
        if not node.children:
            # Node has no children and is not a leaf - shouldn't happen, but handle it
            self.logger.warning(f"Node {node.node_id} has no children and is not a leaf")
            result = self.solver.solve(node.task_description)
            node.set_result(result)
            return result

        # Get results from all children
        sub_results = []
        for child in node.children:
            child_result = self._synthesize_node(child)
            sub_results.append({
                'task': child.task_description,
                'result': child_result
            })

        # Synthesize the results
        try:
            self.logger.debug(f"Synthesizing {len(sub_results)} results for node {node.node_id}")
            result = self.synthesizer.synthesize(node.task_description, sub_results)
            node.set_result(result)
            self.logger.info(f"Node {node.node_id} synthesized successfully")
            return result

        except Exception as e:
            self.logger.error(f"Error synthesizing node {node.node_id}: {e}")
            error = str(e)
            node.set_error(error)
            return f"Error: {error}"

    def get_tree_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the task tree.

        Returns:
            Dictionary with tree statistics
        """
        if not self.tree:
            return {}

        return {
            'total_nodes': len(self.tree.nodes),
            'leaf_nodes': len(self.tree.get_leaf_nodes()),
            'depth': self.tree.get_tree_depth(),
            'completed': self.tree.is_complete(),
            'root_task': self.tree.root.task_description
        }

    def print_results(self):
        """Print the results of all nodes in the tree."""
        if not self.tree:
            self.logger.warning("No tree to print results for")
            return

        self.logger.info("=== Task Tree Results ===")
        self._print_node_results(self.tree.root)

    def _print_node_results(self, node: TaskNode, indent: int = 0):
        """
        Recursively print results for a node and its children.

        Args:
            node: The node to print
            indent: Current indentation level
        """
        prefix = "  " * indent
        result_preview = ""

        if node.result:
            result_preview = f" -> {node.result[:60]}..."
        elif node.error:
            result_preview = f" -> ERROR: {node.error[:60]}..."

        print(f"{prefix}[{node.node_id}] {node.task_description[:50]}{result_preview}")

        for child in node.children:
            self._print_node_results(child, indent + 1)
