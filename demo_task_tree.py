#!/usr/bin/env python3
"""
Demo script for Task Decomposition Tree Agent

This script demonstrates the Task Decomposition Tree agent with a visual example.
"""

import sys
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path('.env')
if env_path.exists():
    load_dotenv(env_path)
    print("📄 Loaded configuration from .env file")
else:
    print("⚠️  No .env file found - using environment variables")

# Verify API keys
if not os.getenv('AWS_ACCESS_KEY_ID') or not os.getenv('AWS_SECRET_ACCESS_KEY') or not os.getenv('AWS_SESSION_TOKEN'):
    print("⚠️  AWS API keys are missing. Please set up your .env file.\n")
    sys.exit(1)

# Add project root to path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from utils.logging_utils import setup_logging
from agent.task_orchestrator import TaskOrchestrator


def print_header(text):
    """Print a formatted header."""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")


def demo_task_tree():
    """Demonstrate the Task Decomposition Tree with a sample task."""

    print_header("TASK DECOMPOSITION TREE DEMO")

    # Setup logging (set to INFO to see the process)
    setup_logging()
    logger = logging.getLogger(__name__)

    print("This demo shows how the Task Decomposition Tree Agent works.")
    print("The agent uses three phases to solve complex tasks:\n")
    print("  1. 🌳 DECOMPOSITION: Break the task into smaller sub-tasks (top-down)")
    print("  2. ✓  VERIFICATION: Validate decomposition and identify leaf nodes")
    print("  3. 🔄 SYNTHESIS: Execute leaves and merge results (bottom-up)\n")

    # Get task from user or use default
    default_task = "How do I make breakfast?"
    print(f"Default task: '{default_task}'")
    user_task = input("Enter your task (or press Enter for default): ").strip()

    task = user_task if user_task else default_task

    print_header(f"PROCESSING: {task}")

    try:
        # Initialize the orchestrator
        print("Initializing Task Decomposition Tree Orchestrator...")
        orchestrator = TaskOrchestrator()
        print("✓ Orchestrator initialized\n")

        # Process the task
        print("Starting three-phase processing...\n")
        result = orchestrator.process_task(task)

        # Print the tree structure
        print_header("TASK TREE STRUCTURE")
        orchestrator.tree.print_tree()

        # Print statistics
        summary = orchestrator.get_tree_summary()
        print_header("TREE STATISTICS")
        print(f"Total Nodes:      {summary['total_nodes']}")
        print(f"Leaf Nodes:       {summary['leaf_nodes']}")
        print(f"Tree Depth:       {summary['depth']}")
        print(f"Fully Completed:  {summary['completed']}")

        # Print the final result
        print_header("FINAL RESULT")
        print(result)
        print()

        # Optionally print detailed results
        print("\nWould you like to see detailed results for each node? (y/n): ", end="")
        show_details = input().strip().lower()

        if show_details == 'y':
            print_header("DETAILED NODE RESULTS")
            orchestrator.print_results()

    except Exception as e:
        logger.error(f"Demo failed: {e}", exc_info=True)
        print(f"\n❌ Error: {e}\n")


def main():
    """Run the demo."""
    try:
        demo_task_tree()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user\n")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}\n")


if __name__ == "__main__":
    main()
