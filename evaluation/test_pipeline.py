#!/usr/bin/env python3
"""
Quick test of the evaluation pipeline.
Tests with just a few prompts to verify everything works.
"""

import subprocess
import sys
import os

def test_evaluation_entry_point():
    """Test that the evaluation entry point works."""

    print("=" * 70)
    print("TESTING EVALUATION PIPELINE")
    print("=" * 70)

    # Test 1: Simple arithmetic with task-decomposition-tree
    print("\nTest 1: Simple Arithmetic (Task Decomposition Tree)")
    print("-" * 70)

    prompt = "What is 2 + 2?"
    agent_type = "task-decomposition-tree"

    print(f"Prompt: {prompt}")
    print(f"Agent: {agent_type}")
    print(f"Running...", flush=True)

    try:
        result = subprocess.run(
            [sys.executable, 'evaluation_entry_point.py', prompt, agent_type],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=120,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )

        if result.returncode == 0:
            output = result.stdout.strip()
            print(f"\n✓ Success!")
            print(f"Output:\n{output}\n")
        else:
            print(f"\n✗ Failed with return code {result.returncode}")
            print(f"Error: {result.stderr}")

    except subprocess.TimeoutExpired:
        print("\n✗ Test timed out")
    except Exception as e:
        print(f"\n✗ Test failed: {e}")

    print("-" * 70)

    # Test 2: Simple question with tree-of-thought-agent
    print("\nTest 2: Simple Question (Tree of Thought Agent)")
    print("-" * 70)

    prompt = "What is the capital of France?"
    agent_type = "tree-of-thought-agent"

    print(f"Prompt: {prompt}")
    print(f"Agent: {agent_type}")
    print(f"Running...", flush=True)

    try:
        result = subprocess.run(
            [sys.executable, 'evaluation_entry_point.py', prompt, agent_type],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=60,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )

        if result.returncode == 0:
            output = result.stdout.strip()
            print(f"\n✓ Success!")
            print(f"Output:\n{output}\n")
        else:
            print(f"\n✗ Failed with return code {result.returncode}")
            print(f"Error: {result.stderr}")

    except subprocess.TimeoutExpired:
        print("\n✗ Test timed out")
    except Exception as e:
        print(f"\n✗ Test failed: {e}")

    print("-" * 70)

    print("\n" + "=" * 70)
    print("PIPELINE TESTS COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    test_evaluation_entry_point()
