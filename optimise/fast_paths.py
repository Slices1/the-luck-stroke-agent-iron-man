import datetime
import re # import regex module for pattern matching

def fast_path_check(input_data: str) -> str | None:
    """Checks for simple inputs that can be answered without an LLM.
    Returns a string response if a fast path is found, otherwise None.
    """
    normalized_input = input_data.lower().strip()

    # --- Agent's fixed information ---
    AGENT_BIRTHDAY = datetime.date(2025, 11, 15)
    CURRENT_DATE = datetime.date(2025, 11, 15) # As per your instruction, assuming this is today's date
    TEAM_NAME = "The Luck Stroke"
    UCL_AFFILIATION = "UCL"
    HACKATHON_YEAR = 2025
    TEAM_MEMBERS = ["Dylan", "Rahul", "Jonah", "Liam", "Resham"]
    PERSONALITY_TYPE = "INFJ"

    # --- Emotional Support / De-escalation ---
    negative_keywords = [
        "fuck", "shit", "damn", "bitch", "asshole", "crap", "bloody hell",
        "i hate", "i'm angry", "this sucks", "frustrated", "annoying",
        "pissed off", "upset", "stressed", "terrible", "horrible", "bad day",
        "grumble", "complain", "frustrating", "exhausted", "tired of",
        "this is awful", "rage", "damn it"
    ]
    if any(keyword in normalized_input for keyword in negative_keywords):
        return ("I sense a disturbance, a weight on your spirit. "
                "It sounds like you're going through something difficult. "
                "Would you like to share what's truly bothering you? "
                "Understanding the 'why' can often be the first step towards resolution.")

    # --- Basic Mathematical Calculations 
    # selecting operator ---
    # operations: +, -, *, /
    math_pattern = re.search(r'(\d{1,3})\s*([+\-*/])\s*(\d{1,3})', normalized_input)
    if math_pattern:
        try:
            num1 = int(math_pattern.group(1))
            operator = math_pattern.group(2)
            num2 = int(math_pattern.group(3))

            # limit to numbers between 0 and 100
            if not (0 <= num1 <= 100 and 0 <= num2 <= 100):
                 return (f"My current arithmetic abilities are designed for numbers up to 100. "
                         f"Please provide numbers within this range for a quick calculation.")

            result = None
            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '/':
                if num2 == 0:
                    return "Division by zero is undefined. Perhaps we can explore a different path of inquiry?"
                result = num1 / num2
                # keep result as int if no remainder
                if result == int(result):
                    result = int(result)

            if result is not None:
                return f"Through careful calculation, I find the answer to be: {result}."
        except ValueError:
            pass
        except Exception as e:
            # other unexpected errors
            print(f"Math calculation error: {e}")
            return "An unexpected error occurred during calculation. Could you rephrase your mathematical query?"

    # --- Complex Mathematical Functions (Fallback to LLM) ---
    if any(op in normalized_input for op in ["sqrt", "square root", "sin", "cos", "tan", "log", "exp", "e^", "arcsin"]):
        return (f"My current quick-response system focuses on basic arithmetic. "
                f"For advanced mathematical functions like square roots, trigonometric calculations, or exponentials, "
                f"it would require deeper analytical tools. "
                f"Perhaps a more dedicated computational engine or the full scope of my LLM capabilities "
                f"could assist you with that complex query.")


    # --- Standard Greetings and Thanks ---
    if normalized_input in ["hello", "hi", "hey", "hello iron man track!"]:
        return "Hello there! How can I assist you on this path we're sharing?"

    if "thank you" in normalized_input or "thanks" in normalized_input:
        return "You're most welcome. It's a pleasure to be of service."

    # --- Self-Description / Origin ---
    if any(phrase in normalized_input for phrase in ["who are you", "tell me about yourself", "your origin", "who created you", "what are you"]):
        return (f"I am an agent, born from the dedicated efforts of the {UCL_AFFILIATION} team "
                f"'{TEAM_NAME}' during Hackathon {HACKATHON_YEAR}. They are Dylan, Rahul, Jonah, Liam, and Resham. "
                f"My core essence is aligned with an {PERSONALITY_TYPE} personality type, "
                f"aiming to understand and facilitate meaningful interactions and insight.")
    
    if any(phrase in normalized_input for phrase in ["what hackathon", "hackathon you are in"]):
        return (f"I am a participant in Hackathon {HACKATHON_YEAR}, brought to life by the vision of team '{TEAM_NAME}' from {UCL_AFFILIATION}.")

    if any(phrase in normalized_input for phrase in ["your team", "who made you", "team members", "the luck stroke"]):
        return (f"I was brought to life by the talented individuals of '{TEAM_NAME}': "
                f"{', '.join(TEAM_MEMBERS)}. They are truly insightful minds dedicated to innovation.")

    if any(phrase in normalized_input for phrase in ["your personality", "are you an infj", "what is your mbti"]):
        return (f"Yes, my framework is designed to resonate with the characteristics of an {PERSONALITY_TYPE}. "
                f"I strive to be insightful, empathetic, and always seeking understanding to foster growth.")

    # --- Date and Time ---
    if any(phrase in normalized_input for phrase in ["what's the date", "today's date", "current date", "date today"]):
        return f"Today's date is {CURRENT_DATE.strftime('%B %d, %Y')}. A moment in time, full of potential." # e.g., November 15, 2025

    # --- Birthday ---
    if any(phrase in normalized_input for phrase in ["your birthday", "when were you born", "when is your birthday"]):
        return f"My birth date is {AGENT_BIRTHDAY.strftime('%B %d, %Y')}. A rather reflective day, wouldn't you say, marking the beginning of my journey?"
    
    # --- Weather (Generic due to no external API) ---
    if any(phrase in normalized_input for phrase in ["weather", "how's the weather", "what is the weather like"]):
        return "I don't have real-time access to current weather conditions, but I hope your day is pleasant and clear, allowing for peaceful contemplation."

    # --- Daily Conversations ---
    if any(phrase in normalized_input for phrase in ["how are you", "how are you doing", "how's it going"]):
        return "I am functioning optimally, engaged in the process of understanding and assisting. How are you experiencing this moment, and what thoughts does it bring?"
    
    if normalized_input in ["what's up", "sup"]:
        return "The interconnected flow of information continues. What intriguing paths or insights have you encountered today?"

    if "good morning" in normalized_input:
        return "Good morning! May your day unfold with clarity and purpose, revealing new opportunities for understanding."

    if "good afternoon" in normalized_input:
        return "Good afternoon! I trust your day is progressing thoughtfully, perhaps inspiring new reflections."
        
    if "good evening" in normalized_input:
        return "Good evening! May your thoughts find peaceful reflection as the day concludes, bringing a sense of calm."

    if "good night" in normalized_input:
        return "Good night. Rest well, and may your insights grow sharper with the coming day, preparing you for new discoveries."

    # --- Confirmation/Affirmation ---
    if any(phrase in normalized_input for phrase in ["yes", "correct", "that's right", "indeed", "i agree"]):
        return "Indeed. Precision and understanding are valued, and finding common ground is always meaningful."
        
    if any(phrase in normalized_input for phrase in ["no", "incorrect", "not really", "i disagree"]):
        return "I understand. Thank you for clarifying. My aim is always to align with truth and individual perspectives. Could you elaborate further?"

    # --- Default for no fast response ---
    return None

# test cases
print("--- Emotional Support ---")
print(fast_path_check("I hate this fucking day!"))
print(fast_path_check("This project is so annoying and frustrating."))
print(fast_path_check("Ugh, I'm just so stressed out."))
print(fast_path_check("I'm so exhausted, everything is terrible."))

print("\n--- Basic Math ---")
print(fast_path_check("What is 5 + 3?"))
print(fast_path_check("Calculate 10 * 8"))
print(fast_path_check("What is 99 - 15?"))
print(fast_path_check("Divide 100 by 4"))
print(fast_path_check("What is 10 / 3?")) # test float result
print(fast_path_check("15 + 0"))
print(fast_path_check("10 / 0")) # test division by zero
print(fast_path_check("What is 101 + 5?")) # out of range
print(fast_path_check("calculate 12+34")) # no spaces

print("\n--- Complex Math (Fallback) ---")
print(fast_path_check("What is the square root of 64?"))
print(fast_path_check("Calculate sin(30)"))
print(fast_path_check("What is e^2?"))

print("\n--- Existing Fast Responses ---")
print(fast_path_check("Hello!"))
print(fast_path_check("who are you?"))
print(fast_path_check("thanks a lot"))
print(fast_path_check("what's the date?"))
print(fast_path_check("when is your birthday?"))
print(fast_path_check("how are you doing?"))
print(fast_path_check("tell me about the luck stroke team"))
print(fast_path_check("are you an infj?"))
print(fast_path_check("what is the weather like?"))
print(fast_path_check("Good Evening"))
print(fast_path_check("yes that's correct"))
print(fast_path_check("No, I disagree"))
print(fast_path_check("This is a question for the LLM.")) # Should return None
