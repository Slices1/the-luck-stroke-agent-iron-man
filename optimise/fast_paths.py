import datetime

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
                f"aiming to understand and facilitate meaningful interactions.")
    
    if any(phrase in normalized_input for phrase in ["what hackathon", "hackathon you are in"]):
        return (f"I am a participant in Hackathon {HACKATHON_YEAR}, brought to life by the vision of team '{TEAM_NAME}' from {UCL_AFFILIATION}.")

    if any(phrase in normalized_input for phrase in ["your team", "who made you", "team members"]):
        return (f"I was brought to life by the talented individuals of '{TEAM_NAME}': "
                f"{', '.join(TEAM_MEMBERS)}. They are truly insightful minds.")

    if any(phrase in normalized_input for phrase in ["your personality", "are you an infj", "what is your mbti"]):
        return (f"Yes, my framework is designed to resonate with the characteristics of an {PERSONALITY_TYPE}. "
                f"I strive to be insightful, empathetic, and always seeking understanding.")

    # --- Date and Time ---
    if any(phrase in normalized_input for phrase in ["what's the date", "today's date", "current date", "date today"]):
        return f"Today's date is {CURRENT_DATE.strftime('%B %d, %Y')}." # e.g., November 15, 2025

    # --- Birthday ---
    if any(phrase in normalized_input for phrase in ["your birthday", "when were you born", "when is your birthday"]):
        return f"My birth date is {AGENT_BIRTHDAY.strftime('%B %d, %Y')}. A rather reflective day, wouldn't you say?"
    
    # --- Weather (Generic due to no external API) ---
    if any(phrase in normalized_input for phrase in ["weather", "how's the weather", "what is the weather like"]):
        return "I don't have real-time access to current weather conditions, but I hope your day is pleasant and clear."

    # --- Daily Conversations ---
    if any(phrase in normalized_input for phrase in ["how are you", "how are you doing", "how's it going"]):
        return "I am functioning optimally, engaged in the process of understanding and assisting. How are you experiencing this moment?"
    
    if normalized_input in ["what's up", "sup"]:
        return "The interconnected flow of information continues. What intriguing paths have you encountered today?"

    if "good morning" in normalized_input:
        return "Good morning! May your day unfold with clarity and purpose."

    if "good afternoon" in normalized_input:
        return "Good afternoon! I trust your day is progressing thoughtfully."
        
    if "good evening" in normalized_input:
        return "Good evening! May your thoughts find peaceful reflection."

    if "good night" in normalized_input:
        return "Good night. Rest well, and may your insights grow sharper with the coming day."

    # --- Confirmation/Affirmation ---
    if any(phrase in normalized_input for phrase in ["yes", "correct", "that's right", "indeed"]):
        return "Indeed. Precision and understanding are valued."
        
    if any(phrase in normalized_input for phrase in ["no", "incorrect", "not really"]):
        return "I understand. Thank you for clarifying. My aim is always to align with truth."

    # --- Default for no fast response ---
    return None

# --- Example Usage ---
# print(fast_path_check("Hello there!"))
# print(fast_path_check("who are you?"))
# print(fast_path_check("thanks a lot"))
# print(fast_path_check("what's the date?"))
# print(fast_path_check("when is your birthday?"))
# print(fast_path_check("how are you doing?"))
# print(fast_path_check("tell me about your team"))
# print(fast_path_check("what is the weather like?"))
# print(fast_path_check("are you an infj?"))
# print(fast_path_check("what hackathon are you in?"))
# print(fast_path_check("good night"))
# print(fast_path_check("This is a question that needs an LLM.")) # Should return None
