#!/usr/bin/env python3
"""
Comprehensive Benchmark Evaluation System

Evaluates all agents at all difficulty levels (L1, L2, L3) and saves results.
"""

import json
import subprocess
import requests
import time
import sys
import os
from datetime import datetime
from collections import defaultdict
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)

# --- LLM Verifier Configuration ---
LLM_VERIFIER_URL = "https://ctwa92wg1b.execute-api.us-east-1.amazonaws.com/prod/invoke"
LLM_VERIFIER_HEADERS = {
    "Content-Type": "application/json"
}

# Get credentials from environment variables
VERIFIER_TEAM_ID = os.getenv('VERIFIER_TEAM_ID')
VERIFIER_API_TOKEN = os.getenv('VERIFIER_API_TOKEN')

if not VERIFIER_TEAM_ID or not VERIFIER_API_TOKEN:
    print("Error: VERIFIER_TEAM_ID and VERIFIER_API_TOKEN must be set in .env file")
    sys.exit(1)

LLM_VERIFIER_PAYLOAD = {
    "team_id": VERIFIER_TEAM_ID,
    "api_token": VERIFIER_API_TOKEN,
    "model": "anthropic.claude-3-5-sonnet-20241022-v2:0",
    "messages": [{"role": "user", "content": ""}],
    "max_tokens": 10
}

# --- Configuration ---
AGENTS_TO_TEST = [
    'tree-of-thought-agent',
    'standard-agent',
    'task-decomposition-tree'
]

LEVELS = ['L1', 'L2', 'L3']

TIMEOUT_PER_PROMPT = 120  # 2 minutes per prompt


def check_answer_with_llm(agent_output, correct_answer):
    """
    Uses an LLM to verify if the agent's output matches the expected answer.
    Returns (is_passed, verification_cost).
    """

    verification_prompt = f"""You are an evaluation "Verifier" agent. Your job is to determine if the "Agent Output" correctly answers the "Expected Answer".

The "Agent Output" does not need to be an exact match, but it must be semantically correct and provide the same information.

Respond with only the word "PASSED" or "FAILED".

---
Expected Answer:
"{correct_answer}"
---
Agent Output:
"{agent_output}"
---
"""

    try:
        payload = json.loads(json.dumps(LLM_VERIFIER_PAYLOAD))
        payload["messages"][0]["content"] = verification_prompt

        response = requests.post(LLM_VERIFIER_URL, headers=LLM_VERIFIER_HEADERS, json=payload, timeout=20)
        response.raise_for_status()

        response_json = response.json()

        # Extract verification cost if available
        verification_cost = 0.0
        if 'metadata' in response_json and 'cost_usd' in response_json['metadata']:
            verification_cost = response_json['metadata']['cost_usd']

        # Extract the text content
        if 'content' in response_json and isinstance(response_json['content'], list) and len(response_json['content']) > 0:
            if 'text' in response_json['content'][0]:
                response_text = response_json['content'][0]['text'].strip().upper()
                if "PASSED" in response_text:
                    return True, verification_cost
                elif "FAILED" in response_text:
                    return False, verification_cost
                else:
                    print(f"  [Verifier Warning] Ambiguous response: {response_text}")
                    return False, verification_cost

        print(f"  [Verifier Error] Unexpected response format")
        return False, verification_cost

    except requests.exceptions.RequestException as e:
        print(f"  [Verifier Error] API request failed: {e}")
        return False, 0.0
    except Exception as e:
        print(f"  [Verifier Error] Unknown error: {e}")
        return False, 0.0


def run_evaluation_for_agent_and_level(agent_type, level, prompts_data, answers_data):
    """
    Run evaluation for a specific agent at a specific level.

    Returns:
        Dictionary with metrics for this agent/level combination
    """
    print(f"\n{'=' * 70}")
    print(f"EVALUATING: {agent_type} at {level}")
    print(f"{'=' * 70}\n")

    # Filter tasks for this level
    level_tasks = {k: v for k, v in prompts_data.items() if k.startswith(level + ':')}

    if not level_tasks:
        print(f"No tasks found for level {level}")
        return None

    total_prompts = 0
    total_successes = 0
    total_agent_time = 0.0
    total_agent_cost = 0.0
    total_verification_cost = 0.0
    failed_prompts = []

    for task_title in level_tasks:
        if task_title not in answers_data:
            print(f"Warning: Skipping '{task_title}' - no answers found.")
            continue

        print(f"\n--- Task: {task_title} ---")

        prompts = prompts_data[task_title]
        answers = answers_data[task_title]

        for i, (prompt, correct_answer) in enumerate(zip(prompts, answers)):
            total_prompts += 1
            print(f"  [{total_prompts}] Running prompt {i+1}/{len(prompts)}...", end=' ', flush=True)

            try:
                # Run the evaluation entry point with agent type
                start_time = time.time()
                result = subprocess.run(
                    [sys.executable, 'evaluation_entry_point.py', prompt, agent_type],
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    timeout=TIMEOUT_PER_PROMPT,
                    check=True,
                    cwd=os.path.dirname(os.path.abspath(__file__))
                )
                end_time = time.time()

                output = result.stdout.strip()

                # Parse agent output
                agent_answer = ""
                task_cost = 0.0
                task_time = end_time - start_time

                if not output:
                    print("AGENT ERROR (no output)")
                    failed_prompts.append({
                        'task': task_title,
                        'prompt': prompt,
                        'expected': correct_answer,
                        'got': '',
                        'error': 'No output from agent'
                    })
                    continue

                lines = output.splitlines()
                try:
                    # Last line should be JSON metrics
                    metrics = json.loads(lines[-1])
                    task_cost = metrics.get('cost', 0.0)
                    task_time = metrics.get('time', task_time)
                    agent_answer = "\n".join(lines[:-1])
                except (json.JSONDecodeError, IndexError):
                    # If no JSON, entire output is the answer
                    agent_answer = output

                total_agent_time += task_time
                total_agent_cost += task_cost

                # Verify the answer
                is_success, verification_cost = check_answer_with_llm(agent_answer, correct_answer)
                total_verification_cost += verification_cost

                if is_success:
                    total_successes += 1
                    print(f"✓ PASS (${task_cost:.6f}, {task_time:.2f}s)")
                else:
                    print(f"✗ FAIL")
                    failed_prompts.append({
                        'task': task_title,
                        'prompt': prompt[:100] + '...' if len(prompt) > 100 else prompt,
                        'expected': correct_answer,
                        'got': agent_answer[:100] + '...' if len(agent_answer) > 100 else agent_answer
                    })

            except subprocess.TimeoutExpired:
                print(f"✗ TIMEOUT")
                failed_prompts.append({
                    'task': task_title,
                    'prompt': prompt[:100] + '...' if len(prompt) > 100 else prompt,
                    'expected': correct_answer,
                    'got': '',
                    'error': 'Timeout'
                })
            except subprocess.CalledProcessError as e:
                print(f"✗ AGENT ERROR")
                print(f"    {e.stderr[:200] if e.stderr else 'Unknown error'}")
                failed_prompts.append({
                    'task': task_title,
                    'prompt': prompt[:100] + '...' if len(prompt) > 100 else prompt,
                    'expected': correct_answer,
                    'got': '',
                    'error': f'Agent crashed: {e.stderr[:100] if e.stderr else "Unknown"}'
                })
            except Exception as e:
                print(f"✗ ERROR: {str(e)[:100]}")
                failed_prompts.append({
                    'task': task_title,
                    'prompt': prompt[:100] + '...' if len(prompt) > 100 else prompt,
                    'expected': correct_answer,
                    'got': '',
                    'error': str(e)[:100]
                })

    # Calculate metrics
    if total_prompts > 0:
        success_rate = (total_successes / total_prompts) * 100
        avg_time = total_agent_time / total_prompts
        avg_cost = total_agent_cost / total_prompts
        total_cost = total_agent_cost + total_verification_cost

        metrics = {
            'agent_type': agent_type,
            'level': level,
            'total_prompts': total_prompts,
            'successes': total_successes,
            'failures': total_prompts - total_successes,
            'success_rate_percent': round(success_rate, 2),
            'avg_time_per_prompt_seconds': round(avg_time, 3),
            'avg_cost_per_prompt_usd': round(avg_cost, 6),
            'total_agent_cost_usd': round(total_agent_cost, 6),
            'total_verification_cost_usd': round(total_verification_cost, 6),
            'total_cost_usd': round(total_cost, 6),
            'failed_prompts': failed_prompts
        }

        # Print summary
        print(f"\n{'-' * 70}")
        print(f"RESULTS for {agent_type} at {level}:")
        print(f"  Success Rate:      {total_successes}/{total_prompts} ({success_rate:.2f}%)")
        print(f"  Avg Time/Prompt:   {avg_time:.3f}s")
        print(f"  Avg Cost/Prompt:   ${avg_cost:.6f}")
        print(f"  Total Cost:        ${total_cost:.6f}")
        print(f"{'-' * 70}")

        return metrics
    else:
        print("\nNo prompts were evaluated.")
        return None


def run_full_benchmark():
    """
    Run the complete benchmark across all agents and levels.
    """
    print("\n" + "=" * 70)
    print("COMPREHENSIVE BENCHMARK EVALUATION")
    print("=" * 70)

    # Load prompts and answers
    script_dir = os.path.dirname(os.path.abspath(__file__))
    prompts_file = os.path.join(script_dir, 'benchmark_prompts.json')
    answers_file = os.path.join(script_dir, 'benchmark_answers.json')

    try:
        with open(prompts_file, 'r', encoding='utf-8') as f:
            prompts_data = json.load(f)
        with open(answers_file, 'r', encoding='utf-8') as f:
            answers_data = json.load(f)
    except FileNotFoundError:
        print("Error: Benchmark files not found.")
        print(f"Expected: {prompts_file} and {answers_file}")
        return
    except json.JSONDecodeError:
        print("Error: JSON files are corrupted.")
        return

    # Store all results
    all_results = {
        'timestamp': datetime.now().isoformat(),
        'agents': AGENTS_TO_TEST,
        'levels': LEVELS,
        'results': []
    }

    # Run evaluation for each agent at each level
    for agent_type in AGENTS_TO_TEST:
        for level in LEVELS:
            metrics = run_evaluation_for_agent_and_level(agent_type, level, prompts_data, answers_data)
            if metrics:
                all_results['results'].append(metrics)

    # Save results to file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_file = os.path.join(script_dir, f'benchmark_results_{timestamp}.json')

    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2)

    print(f"\n{'=' * 70}")
    print(f"BENCHMARK COMPLETE")
    print(f"Results saved to: {results_file}")
    print(f"{'=' * 70}\n")

    # Print summary table
    print_summary_table(all_results)


def print_summary_table(all_results):
    """
    Print a summary table of all results.
    """
    print("\n" + "=" * 70)
    print("SUMMARY TABLE")
    print("=" * 70)
    print(f"\n{'Agent':<30} {'Level':<8} {'Success%':<12} {'Avg Time':<12} {'Avg Cost':<12}")
    print("-" * 70)

    for result in all_results['results']:
        agent = result['agent_type']
        level = result['level']
        success_rate = result['success_rate_percent']
        avg_time = result['avg_time_per_prompt_seconds']
        avg_cost = result['avg_cost_per_prompt_usd']

        print(f"{agent:<30} {level:<8} {success_rate:>6.2f}%     {avg_time:>7.3f}s     ${avg_cost:>9.6f}")

    print("=" * 70 + "\n")


if __name__ == "__main__":
    run_full_benchmark()
