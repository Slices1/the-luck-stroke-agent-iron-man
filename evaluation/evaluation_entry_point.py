#!/usr/bin/env python3
"""
Evaluation Entry Point for Benchmark Testing

This script is called by evaluate_benchmark.py for each prompt.
It integrates with the actual agent implementations.
"""

import sys
import os
import json
import time

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(project_root) / '.env'
if env_path.exists():
    load_dotenv(env_path)

from agent.controller import AgentController


# Simple model pricing (USD per 1K tokens)
# These are approximate - adjust based on actual pricing
MODEL_PRICING = {
    'anthropic.claude-3-5-sonnet-20240620-v1:0': {'input': 0.003, 'output': 0.015},
    'anthropic.claude-3-haiku-20240307-v1:0': {'input': 0.00025, 'output': 0.00125},
    'us.amazon.nova-lite-v1:0': {'input': 0.00006, 'output': 0.00024},
}


def estimate_tokens(text):
    """
    Rough token estimation (1 token ≈ 4 characters).
    This is a simplification - real token count varies by model.
    """
    return len(text) // 4


def estimate_cost(prompt, response, model):
    """
    Estimate the cost of an LLM call.
    """
    if model not in MODEL_PRICING:
        return 0.0

    pricing = MODEL_PRICING[model]
    input_tokens = estimate_tokens(prompt)
    output_tokens = estimate_tokens(response)

    input_cost = (input_tokens / 1000) * pricing['input']
    output_cost = (output_tokens / 1000) * pricing['output']

    return input_cost + output_cost


def get_agent_response(prompt, agent_type='task-decomposition-tree'):
    """
    Get response from the specified agent.

    Args:
        prompt: The prompt/question to send to the agent
        agent_type: Which agent to use (tree-of-thought-agent, standard-agent, task-decomposition-tree)

    Returns:
        final_answer: The agent's response
        metrics: Dictionary with cost and time metrics
    """
    start_time = time.time()

    try:
        # Initialize the agent
        agent = AgentController(config=None, agent_type=agent_type)

        # Get the response
        response = agent.run_step(prompt)

        end_time = time.time()
        processing_time = end_time - start_time

        # Estimate cost based on agent type
        # For task-decomposition-tree: uses Haiku + Nova Lite
        # For tree-of-thought-agent: uses Sonnet
        # For standard-agent: uses dynamic selection
        estimated_cost = 0.0

        if agent_type == 'task-decomposition-tree':
            # Rough estimate: multiple Haiku calls + Nova Lite calls
            # Assume average of 8 Haiku calls and 5 Nova Lite calls per prompt
            estimated_cost += estimate_cost(prompt, response, 'anthropic.claude-3-haiku-20240307-v1:0') * 8
            estimated_cost += estimate_cost(prompt, response, 'us.amazon.nova-lite-v1:0') * 5
        elif agent_type == 'tree-of-thought-agent':
            # Single Sonnet call
            estimated_cost = estimate_cost(prompt, response, 'anthropic.claude-3-5-sonnet-20240620-v1:0')
        elif agent_type == 'standard-agent':
            # Dynamic - assume average uses Haiku
            estimated_cost = estimate_cost(prompt, response, 'anthropic.claude-3-haiku-20240307-v1:0')

        metrics = {
            "cost": estimated_cost,
            "time": processing_time,
            "agent_type": agent_type
        }

        # Convert response to string if it's an AgentResult
        final_answer = str(response).strip()

        return final_answer, metrics

    except Exception as e:
        # If agent fails, return error and zero metrics
        end_time = time.time()
        processing_time = end_time - start_time

        metrics = {
            "cost": 0.0,
            "time": processing_time,
            "agent_type": agent_type,
            "error": str(e)
        }

        return f"ERROR: {str(e)}", metrics


def main():
    """
    Main entry point for evaluation.
    Reads prompt and agent type from command-line arguments.
    """

    if len(sys.argv) < 2:
        print("Error: No prompt provided as argument.", file=sys.stderr)
        sys.exit(1)

    prompt = sys.argv[1]

    # Optional: specify agent type as second argument
    agent_type = 'task-decomposition-tree'  # default
    if len(sys.argv) >= 3:
        agent_type = sys.argv[2]

    # Get the agent's response
    final_answer, metrics = get_agent_response(prompt, agent_type)

    # Print the final answer to stdout
    print(final_answer)

    # Print the metrics JSON on the last line
    print(json.dumps(metrics))


if __name__ == "__main__":
    main()
