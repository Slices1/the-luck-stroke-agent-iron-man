import sys
import json
import time
import random

def get_agent_response(prompt):
    """
    --- THIS IS THE MOCKUP ---
    Replace this function with your actual "Branching Minds" agent logic.
    
    Your agent logic must:
    1. Take the `prompt` string as input.
    2. Perform its decomposition, verification, and synthesis.
    3. Return two things:
       - The final string answer.
       - A dictionary containing its internal metrics.
    """
    
    # Simulate work
    processing_time = random.uniform(0.5, 3.0)
    time.sleep(processing_time)
    
    # Simulate cost (e.g., token count * price)
    # (Update this with your agent's actual token usage)
    simulated_cost = random.uniform(0.0001, 0.0005)
    
    # --- Mock Logic ---
    # This is a dummy: it just echoes the prompt.
    # Your real agent will produce a real answer.
    if "Reverse this string:" in prompt:
        word = prompt.split("'")[1]
        final_answer = word[::-1] # Mock correct answer
    elif "What is" in prompt:
        try:
            parts = prompt.replace("What is", "").replace("?", "").strip()
            final_answer = str(eval(parts)) # Mock correct answer
        except:
            final_answer = "Mock Answer: Could not parse arithmetic."
    else:
        final_answer = f"Mock Answer: The prompt was '{prompt[:20]}...'"
    # --- End Mock Logic ---

    metrics = {
        "cost": simulated_cost,
        "time": processing_time
    }
    
    return final_answer, metrics

def main():
    """
    Main entry point.
    Handles I/O for the evaluation script.
    
    --- DO NOT CHANGE THIS PART ---
    This script is designed to be called by `evaluate_benchmark.py`.
    It reads a prompt from the command-line arguments and prints its
    answer and metrics to stdout in a specific format.
    """
    
    # 1. Read prompt from command-line arguments
    if len(sys.argv) < 2:
        print("Error: No prompt provided as argument.", file=sys.stderr)
        sys.exit(1)
        
    prompt = sys.argv[1]
    
    # 2. Get the agent's response
    final_answer, metrics = get_agent_response(prompt)
    
    # 3. Print the final answer to stdout
    # The evaluator script will read this.
    print(final_answer)
    
    # 4. Print the metrics JSON on the *last* line of stdout
    # The evaluator script will parse this last line.
    print(json.dumps(metrics))

if __name__ == "__main__":
    main()
