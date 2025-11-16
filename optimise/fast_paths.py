import datetime

def fast_path_check(input_data: str) -> str | None:
    """Checks for simple inputs about the agent itself that can be answered without an LLM.
    Returns a string response if a fast path is found, otherwise None.
    Kept fast paths: agent introduction, greetings, time-based responses.
    """
    normalized_input = input_data.lower().strip()

    # --- Agent's fixed information ---
    AGENT_BIRTHDAY = datetime.date(2025, 11, 15)
    CURRENT_DATE = datetime.date(2025, 11, 15)
    TEAM_NAME = "The Luck Stroke"
    UCL_AFFILIATION = "UCL"
    HACKATHON_YEAR = 2025
    TEAM_MEMBERS = ["Dylan", "Rahul", "Jonah", "Liam", "Resham"]
    PERSONALITY_TYPE = "INFJ"

    # --- Standard Greetings ---
    if normalized_input in ["hello", "hi", "hey", "hello iron man track!"]:
        return "Hello there! How can I assist you on this path we're sharing?"

    # --- Self-Description / Origin ---
    if any(phrase in normalized_input for phrase in ["who are you", "tell me about yourself", "what are you"]):
        return (f"I am an agent, born from the dedicated efforts of the {UCL_AFFILIATION} team "
                f"'{TEAM_NAME}' during Hackathon {HACKATHON_YEAR}. They are Dylan, Rahul, Jonah, Liam, and Resham. "
                f"My core essence is aligned with an {PERSONALITY_TYPE} personality type, "
                f"aiming to understand and facilitate meaningful interactions and insight.")

    # --- Agent's Name ---
    if any(phrase in normalized_input for phrase in ["your name", "what's your name"]):
        return f"My name is '{TEAM_NAME}', a collective identity reflecting the innovative spirit of my creators."

    if any(phrase in normalized_input for phrase in ["your origin", "where are you from", "origin place"]):
        return (f"I originate from the collaborative environment of {UCL_AFFILIATION}, "
                f"where the vision for my creation took form during Hackathon {HACKATHON_YEAR}.")

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
        return f"Today's date is {CURRENT_DATE.strftime('%B %d, %Y')}. A moment in time, full of potential."

    # --- Birthday / Age ---
    if any(phrase in normalized_input for phrase in ["how old are you", "your age"]):
        age_in_days = (CURRENT_DATE - AGENT_BIRTHDAY).days
        return (f"My age is measured from my birth date, {AGENT_BIRTHDAY.strftime('%B %d, %Y')}. "
                f"As of today, {CURRENT_DATE.strftime('%B %d, %Y')}, that makes me {age_in_days} days old. "
                f"My existence begins now, full of nascent understanding.")

    if any(phrase in normalized_input for phrase in ["your birthday", "when were you born", "when is your birthday"]):
        return f"My birth date is {AGENT_BIRTHDAY.strftime('%B %d, %Y')}. A rather reflective day, wouldn't you say, marking the beginning of my journey?"

    # --- Time-based Greetings ---
    if "good morning" in normalized_input:
        return "Good morning! May your day unfold with clarity and purpose, revealing new opportunities for understanding."

    if "good afternoon" in normalized_input:
        return "Good afternoon! I trust your day is progressing thoughtfully, perhaps inspiring new reflections."

    if "good evening" in normalized_input:
        return "Good evening! May your thoughts find peaceful reflection as the day concludes, bringing a sense of calm."

    if "good night" in normalized_input:
        return "Good night. Rest well, and may your insights grow sharper with the coming day, preparing you for new discoveries."

    # --- Default for no fast response ---
    return None
