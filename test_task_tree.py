#!/usr/bin/env python3
"""
Test script for Task Decomposition Tree Agent

This script tests the Task Decomposition Tree implementation with a simple example.
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
from agent.controller import TaskDecompositionTreeAgent

def test_simple_task():
    """Test with a simple task that should decompose nicely."""
    print("\n" + "="*60)
    print("TEST: Simple Task Decomposition")
    print("="*60 + "\n")

    # Initialize logging
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        # Initialize the agent
        print("Initializing Task Decomposition Tree Agent...")
        agent = TaskDecompositionTreeAgent()
        print("✓ Agent initialized successfully\n")

        # Test with a simple task
        task = "How do I make a cup of tea?"
        print(f"Task: {task}\n")
        print("-" * 60)

        # Run the agent
        result = agent.run(task)

        print("\n" + "="*60)
        print("RESULT:")
        print("="*60)
        print(result)
        print("\n")

        return True

    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)
        print(f"\n❌ Test failed: {e}\n")
        return False


def test_factual_question():
    """Test with a factual question."""
    print("\n" + "="*60)
    print("TEST: Factual Question")
    print("="*60 + "\n")

    logger = logging.getLogger(__name__)

    try:
        # Initialize the agent
        print("Initializing Task Decomposition Tree Agent...")
        agent = TaskDecompositionTreeAgent()
        print("✓ Agent initialized successfully\n")

        # Test with a factual question
        task = "What is the capital of France?"
        print(f"Task: {task}\n")
        print("-" * 60)

        # Run the agent
        result = agent.run(task)

        print("\n" + "="*60)
        print("RESULT:")
        print("="*60)
        print(result)
        print("\n")

        return True

    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)
        print(f"\n❌ Test failed: {e}\n")
        return False


def test_complex_task():
    """Test with a more complex task."""
    print("\n" + "="*60)
    print("TEST: Complex Task Decomposition")
    print("="*60 + "\n")

    logger = logging.getLogger(__name__)

    try:
        # Initialize the agent
        print("Initializing Task Decomposition Tree Agent...")
        agent = TaskDecompositionTreeAgent()
        print("✓ Agent initialized successfully\n")

        # Test with a complex task
        task = "Explain the water cycle"
        print(f"Task: {task}\n")
        print("-" * 60)

        # Run the agent
        result = agent.run(task)

        print("\n" + "="*60)
        print("RESULT:")
        print("="*60)
        print(result)
        print("\n")

        return True

    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)
        print(f"\n❌ Test failed: {e}\n")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("TASK DECOMPOSITION TREE AGENT - TEST SUITE")
    print("="*60)

    tests = [
        ("Simple Task", test_simple_task),
        ("Factual Question", test_factual_question),
        ("Complex Task", test_complex_task),
    ]

    results = {}

    for test_name, test_func in tests:
        print(f"\n🧪 Running test: {test_name}")
        try:
            success = test_func()
            results[test_name] = "✓ PASSED" if success else "✗ FAILED"
        except Exception as e:
            print(f"❌ Test crashed: {e}")
            results[test_name] = f"✗ CRASHED: {e}"

    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    for test_name, result in results.items():
        print(f"{test_name:30s} {result}")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
