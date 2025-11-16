import json
import subprocess
import requests
import time
import sys

# --- LLM Verifier Configuration ---
# (Based on the script you provided)

LLM_VERIFIER_URL = "https://ctwa92wg1b.execute-api.us-east-1.amazonaws.com/prod/invoke"
LLM_VERIFIER_HEADERS = {
    "Content-Type": "application/json"
}
LLM_VERIFIER_PAYLOAD = {
    "team_id": "team_the_great_hack_2025_006",
    "api_token": "qlv4R56nnTH6CJtrUxPRvCBC6D0MIgbRlyFcUKDPbmA",
    "model": "anthropic.claude-3-5-sonnet-20241022-v2:0",
    "messages": [{"role": "user", "content": ""}], # Content will be set dynamically
    "max_tokens": 10
}

def check_answer_with_llm(agent_output, correct_answer):
    """
    Uses an LLM to verify if the agent's output matches the expected answer.
    Returns True for "PASSED" and False for "FAILED".
    """
    
    # This prompt is engineered to force a simple "PASSED" or "FAILED" response
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
        # Create a deep copy of the payload to avoid modifying the template
        payload = json.loads(json.dumps(LLM_VERIFIER_PAYLOAD))
        payload["messages"][0]["content"] = verification_prompt
        
        response = requests.post(LLM_VERIFIER_URL, headers=LLM_VERIFIER_HEADERS, json=payload, timeout=20)
        response.raise_for_status() # Raise an exception for bad status codes
        
        response_json = response.json()
        
        # Extract the text content from the response
        # This structure depends on the API's response format
        if 'content' in response_json and isinstance(response_json['content'], list) and len(response_json['content']) > 0:
            if 'text' in response_json['content'][0]:
                response_text = response_json['content'][0]['text'].strip().upper()
                if "PASSED" in response_text:
                    return True
                elif "FAILED" in response_text:
                    return False
                else:
                    print(f"  [Verifier Warning] LLM Verifier gave ambiguous response: {response_text}")
                    return False # Default to failure on ambiguity
            else:
                print(f"  [Verifier Error] 'text' key not in response content: {response_json}")
                return False
        else:
            print(f"  [Verifier Error] Unexpected LLM response format: {response_json}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"  [Verifier Error] API request failed: {e}")
        return False
    except json.JSONDecodeError:
        print(f"  [Verifier Error] Failed to decode LLM response: {response.text}")
        return False
    except Exception as e:
        print(f"  [Verifier Error] Unknown error in LLM verifier: {e}")
        return False

def run_evaluation():
    """
    Loads prompts and answers, runs the agent, and evaluates the results.
    """
    try:
        with open('benchmark_prompts.json', 'r', encoding='utf-8') as f:
            prompts_data = json.load(f)
        with open('benchmark_answers.json', 'r', encoding='utf-8') as f:
            answers_data = json.load(f)
    except FileNotFoundError:
        print("Error: 'benchmark_prompts.json' or 'benchmark_answers.json' not found.")
        print("Please run 'generate_prompts.py' first.")
        return
    except json.JSONDecodeError:
        print("Error: JSON files are corrupted.")
        return

    total_prompts = 0
    total_successes = 0
    total_processing_time = 0.0
    total_cost = 0.0

    print("Starting Benchmark Evaluation...")

    for task_title in prompts_data:
        if task_title not in answers_data:
            print(f"Warning: Skipping '{task_title}' - no answers found.")
            continue
        
        print(f"\n--- Running Task: {task_title} ---")
        
        prompts = prompts_data[task_title]
        answers = answers_data[task_title]
        
        for i, (prompt, correct_answer) in enumerate(zip(prompts, answers)):
            total_prompts += 1
            print(f"  [RUNNING] Prompt {i+1}/{len(prompts)}...")
            
            try:
                # 1. Run the external agent script
                # We pass the prompt as a command-line argument
                # The agent script MUST print its answer to stdout
                # and its metrics as a JSON string on the *last* line.
                start_time = time.time()
                result = subprocess.run(
                    [sys.executable, 'evaluation_entry_point.py', prompt],
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    timeout=60, # 60-second timeout per prompt
                    check=True # Raise error if script fails
                )
                end_time = time.time()
                
                output = result.stdout.strip()
                
                # 2. Parse the agent's output
                agent_answer = ""
                task_cost = 0.0
                task_time = end_time - start_time # Default to wall time
                
                if not output:
                    print("  [AGENT ERROR] Agent returned no output.")
                    agent_answer = "" # Treat as empty answer
                else:
                    lines = output.splitlines()
                    try:
                        # Assume last line is JSON metrics
                        metrics = json.loads(lines[-1])
                        task_cost = metrics.get('cost', 0.0)
                        task_time = metrics.get('time', task_time) # Prefer agent's reported time
                        agent_answer = "\n".join(lines[:-1]) # All other lines are the answer
                    except (json.JSONDecodeError, IndexError):
                        # If no JSON line, assume entire output is the answer
                        agent_answer = output
                
                total_processing_time += task_time
                total_cost += task_cost

                # 3. Verify the answer with the LLM
                is_success = check_answer_with_llm(agent_answer, correct_answer)
                
                if is_success:
                    total_successes += 1
                    print(f"  [PASSED] Prompt {i+1}/{len(prompts)} (Cost: ${task_cost:.6f}, Time: {task_time:.2f}s)")
                else:
                    print(f"  [FAILED] Prompt {i+1}/{len(prompts)}")
                    print(f"    - EXPECTED: {correct_answer}")
                    print(f"    - GOT:      {agent_answer.replace(chr(10), ' ')}")

            except subprocess.TimeoutExpired:
                print(f"  [AGENT ERROR] Prompt {i+1}/{len(prompts)} timed out.")
            except subprocess.CalledProcessError as e:
                print(f"  [AGENT ERROR] Prompt {i+1}/{len(prompts)} script failed:")
                print(e.stderr)
            except Exception as e:
                print(f"  [EVAL ERROR] An unexpected error occurred: {e}")

    # --- Final Report ---
    print("\n\n--- Benchmark Complete ---")
    if total_prompts > 0:
        success_rate = (total_successes / total_prompts) * 100
        avg_time = total_processing_time / total_prompts
        
        print(f"Task Success Rate: {total_successes} / {total_prompts} ({success_rate:.2f}%)")
        print(f"Total Cost:        ${total_cost:.6f}")
        print(f"Average Time:      {avg_time:.2f}s per prompt")
    else:
        print("No prompts were run.")

if __name__ == "__main__":
    run_evaluation()
