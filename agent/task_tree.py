"""
Task Decomposition Tree Implementation

This module implements a hierarchical task decomposition system that breaks down
complex tasks into simpler sub-tasks using a tree structure.

The system uses three phases:
1. Decomposition: Break tasks into sub-tasks (top-down)
2. Verification: Validate decompositions and identify leaf nodes (peer review)
3. Synthesis: Execute leaf nodes and merge results (bottom-up)
"""

import logging
import json
from typing import List, Dict, Optional, Any
from enum import Enum


class TaskStatus(Enum):
    """Status of a task node in the tree."""
    PENDING = "pending"           # Not yet processed
    DECOMPOSING = "decomposing"   # Being broken down
    VERIFIED = "verified"         # Decomposition verified
    EXECUTING = "executing"       # Leaf node being executed
    COMPLETED = "completed"       # Task finished
    FAILED = "failed"            # Task failed


class TaskNode:
    """
    Represents a single task node in the Task Decomposition Tree.

    Each node can either be:
    - A parent node with sub-tasks (non-leaf)
    - A leaf node that can be executed directly (atomic task)
    """

    def __init__(self, task_description: str, node_id: str, parent_id: Optional[str] = None):
        """
        Initialize a task node.

        Args:
            task_description: Natural language description of the task
            node_id: Unique identifier for this node
            parent_id: ID of parent node (None for root)
        """
        self.node_id = node_id
        self.parent_id = parent_id
        self.task_description = task_description
        self.status = TaskStatus.PENDING
        self.is_leaf = False  # Determined by verifier
        self.children: List[TaskNode] = []
        self.result: Optional[str] = None
        self.error: Optional[str] = None
        self.metadata: Dict[str, Any] = {}

        self.logger = logging.getLogger(__name__)

    def add_child(self, child: 'TaskNode'):
        """Add a child sub-task to this node."""
        self.children.append(child)
        child.parent_id = self.node_id

    def mark_as_leaf(self):
        """Mark this node as a leaf node (atomic task)."""
        self.is_leaf = True
        self.logger.debug(f"Node {self.node_id} marked as leaf: {self.task_description}")

    def set_result(self, result: str):
        """Set the result for this task."""
        self.result = result
        self.status = TaskStatus.COMPLETED
        self.logger.info(f"Node {self.node_id} completed with result")

    def set_error(self, error: str):
        """Set an error for this task."""
        self.error = error
        self.status = TaskStatus.FAILED
        self.logger.error(f"Node {self.node_id} failed: {error}")

    def to_dict(self) -> Dict[str, Any]:
        """Convert node to dictionary representation."""
        return {
            'node_id': self.node_id,
            'parent_id': self.parent_id,
            'task_description': self.task_description,
            'status': self.status.value,
            'is_leaf': self.is_leaf,
            'children': [child.node_id for child in self.children],
            'result': self.result,
            'error': self.error,
            'metadata': self.metadata
        }

    def __repr__(self):
        return f"TaskNode(id={self.node_id}, task='{self.task_description[:50]}...', status={self.status.value}, is_leaf={self.is_leaf}, children={len(self.children)})"


class TaskDecompositionTree:
    """
    Manages the complete Task Decomposition Tree structure.

    This class handles:
    - Building the tree through recursive decomposition
    - Tracking all nodes
    - Providing tree traversal capabilities
    """

    def __init__(self, root_task: str):
        """
        Initialize the tree with a root task.

        Args:
            root_task: The main task to be decomposed
        """
        self.root = TaskNode(root_task, node_id="root")
        self.nodes: Dict[str, TaskNode] = {"root": self.root}
        self._node_counter = 0
        self.logger = logging.getLogger(__name__)

        self.logger.info(f"Task Decomposition Tree initialized with root task: {root_task}")

    def generate_node_id(self) -> str:
        """Generate a unique node ID."""
        self._node_counter += 1
        return f"node_{self._node_counter}"

    def add_node(self, task_description: str, parent_id: str) -> TaskNode:
        """
        Add a new node to the tree.

        Args:
            task_description: Description of the sub-task
            parent_id: ID of the parent node

        Returns:
            The newly created TaskNode
        """
        if parent_id not in self.nodes:
            raise ValueError(f"Parent node {parent_id} not found in tree")

        node_id = self.generate_node_id()
        node = TaskNode(task_description, node_id, parent_id)

        # Add to parent's children
        parent = self.nodes[parent_id]
        parent.add_child(node)

        # Add to nodes dictionary
        self.nodes[node_id] = node

        self.logger.debug(f"Added node {node_id} as child of {parent_id}: {task_description}")
        return node

    def get_node(self, node_id: str) -> Optional[TaskNode]:
        """Get a node by its ID."""
        return self.nodes.get(node_id)

    def get_leaf_nodes(self) -> List[TaskNode]:
        """Get all leaf nodes in the tree."""
        return [node for node in self.nodes.values() if node.is_leaf]

    def get_pending_nodes(self) -> List[TaskNode]:
        """Get all nodes that are pending (not yet decomposed or executed)."""
        return [node for node in self.nodes.values()
                if node.status == TaskStatus.PENDING and not node.is_leaf]

    def is_complete(self) -> bool:
        """Check if all nodes in the tree are completed."""
        return all(node.status == TaskStatus.COMPLETED for node in self.nodes.values())

    def get_tree_depth(self) -> int:
        """Calculate the maximum depth of the tree."""
        def depth(node: TaskNode) -> int:
            if not node.children:
                return 1
            return 1 + max(depth(child) for child in node.children)
        return depth(self.root)

    def print_tree(self, node: Optional[TaskNode] = None, indent: int = 0):
        """
        Print a visual representation of the tree.

        Args:
            node: Node to start from (defaults to root)
            indent: Current indentation level
        """
        if node is None:
            node = self.root

        prefix = "  " * indent
        leaf_marker = "[LEAF]" if node.is_leaf else ""
        status_marker = f"[{node.status.value}]"

        print(f"{prefix}├─ {node.node_id}: {node.task_description[:60]} {leaf_marker} {status_marker}")

        for child in node.children:
            self.print_tree(child, indent + 1)

    def to_dict(self) -> Dict[str, Any]:
        """Convert entire tree to dictionary representation."""
        return {
            'root': self.root.to_dict(),
            'nodes': {node_id: node.to_dict() for node_id, node in self.nodes.items()},
            'depth': self.get_tree_depth(),
            'total_nodes': len(self.nodes),
            'leaf_nodes': len(self.get_leaf_nodes())
        }

    def __repr__(self):
        return f"TaskDecompositionTree(root='{self.root.task_description[:50]}...', nodes={len(self.nodes)}, depth={self.get_tree_depth()})"
