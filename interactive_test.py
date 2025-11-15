# interactive_test.py
import sys

# Now that interactive_test.py is at the project root,
# 'optimise' is directly importable.
from optimise.fast_paths import fast_path_check

# --- Interactive Test Loop ---
if __name__ == "__main__":
    print("\n--- Agent Interactive Test ---")
    print("Type your queries. Type 'exit' or 'quit' to end the session.")
    print("------------------------------")
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() in ['exit', 'quit']:
            print("Agent: Goodbye for now. May your path be clear.")
            break
        
        response = fast_path_check(user_input)
        
        if response:
            print(f"Agent (Fast Response): {response}")
        else:
            # This simulates what happens if no fast response is found, 
            # implying a fallback to a more capable LLM.
            print("Agent (LLM Fallback): Interesting query. My immediate thoughts don't cover that, but I can delve deeper using my broader analytical capabilities. What precisely are you seeking to understand?")
