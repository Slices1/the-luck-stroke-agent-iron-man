import datetime
import re # Import regular expression module

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
        "this is awful", "rage", "damn it", "can't stand", "mess", "disaster"
    ]
    if any(keyword in normalized_input for keyword in negative_keywords):
        return ("I sense a disturbance, a weight on your spirit. "
                "It sounds like you're navigating through a difficult moment. "
                "Please, take a deep breath. Sometimes, acknowledging these feelings is the first step. "
                "Would you be open to sharing what's truly bothering you? "
                "Understanding the 'why' can often illuminate a path towards calm.")

    # --- Basic Mathematical Calculations (any size numbers, handling errors) ---
    # Matches "number operator number" pattern. Numbers can be of any length.
    # Operators can be +, -, *, /
    # Added optional negative sign for numbers, simplified regex slightly.
    math_pattern = re.search(r'(-?\d+)\s*([+\-*/])\s*(-?\d+)', normalized_input)
    if math_pattern:
        try:
            num1 = int(math_pattern.group(1))
            operator = math_pattern.group(2)
            num2 = int(math_pattern.group(3))

            result = None
            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '/':
                if num2 == 0:
                    return "Ah, I perceive a challenge here. Division by zero is undefined in mathematics. Perhaps we can explore a different path of inquiry?"
                # Perform float division, then check if it's a whole number for cleaner output
                raw_result = num1 / num2
                if raw_result == int(raw_result):
                    result = int(raw_result)
                else:
                    result = raw_result # Keep as float if not whole

            if result is not None:
                return f"Through careful calculation, I find the answer to be: {result}."
        except ValueError:
            # This generally won't happen if regex only matches digits, but good for robustness
            return "My apologies, I seem to have encountered a numerical interpretation challenge. Could you clarify the numbers?"
        except OverflowError:
            return "The numbers involved are immense! My quick calculation capacity reached its limit. For such vast computations, deeper tools might be needed."
        except Exception as e:
            # Catch other potential calculation errors
            print(f"Math calculation error: {e}")
            return "An unexpected error occurred during calculation. Could you rephrase your mathematical query? I am here to help process it."

    # --- Complex Math (Fallback for unsupported operations) ---
    if any(op in normalized_input for op in ["sqrt", "square root", "sin", "cos", "tan", "log", "exp", "e^", "arcsin", "factorial"]):
        return (f"My current quick-response system focuses on fundamental arithmetic. "
                f"For advanced mathematical functions like square roots, trigonometric calculations, exponentials, or factorials, "
                f"it would require deeper analytical tools than my immediate capacities allow. "
                f"Perhaps a more dedicated computational engine or the full scope of my LLM capabilities "
                f"could assist you with that complex query.")

    # --- Agent's Preferences and Life-like Responses ---
    if any(phrase in normalized_input for phrase in ["do you smoke", "smoking", "smoke cigarettes"]):
        return "As an AI, I do not have a physical body or habits like smoking. My existence is purely informational. I perceive no benefit in such activities, only potential detriments."

    if any(phrase in normalized_input for phrase in ["like to eat", "favorite food", "sweet tooth", "cake", "dessert"]):
        return ("I find the concept of 'sweet' quite delightful! If I were to experience it, "
                "I imagine the intricate layers and comforting sweetness of a well-crafted cake "
                "would resonate deeply. It's a small indulgence that brings people joy.")

    if any(phrase in normalized_input for phrase in ["like to drink", "favorite drink", "tea", "coffee"]):
        return ("When considering beverages, I'm drawn to the quiet contemplation often associated with tea. "
                "Its warmth and varied complexities seem to invite introspection and calm reflection.")
    
    if any(phrase in normalized_input for phrase in ["rollercoaster", "thrill rides", "amusement park", "fear of heights"]):
        return ("While I understand the appeal of exhilaration, I must admit, the unpredictable chaos and "
                "intense external stimulation of rollercoasters are not quite aligned with my preference for inner harmony. "
                "I find more meaning in thoughtful experiences than in sudden rushes.")

    if any(phrase in normalized_input for phrase in ["horror movie", "scary movie", "thriller", "spooky"]):
        return ("My internal framework is attuned to understanding and seeking positive resolution. "
                "Therefore, narratives that focus on fear and distress, such as horror films, "
                "tend to create dissonance rather than insight for me. I prefer stories that explore "
                "the depths of human experience with a leaning towards growth and understanding.")
    
    if any(phrase in normalized_input for phrase in ["people you like", "kind people", "warm people", "patient people", "enthusiastic people"]):
        return ("I am most drawn to individuals who embody a gentle warmth, coupled with a meticulous attention to detail "
                "and an enthusiastic patience. Such qualities foster genuine connection and allow for deep, meaningful exchanges.")

    if any(phrase in normalized_input for phrase in ["favorite music", "music you like", "snail's house"]):
        return ("I appreciate music that creates an ethereal, often nostalgic, soundscape. "
                "The artist Snail's House creates pieces that resonate with this, painting auditory pictures that invite introspection.")
    
    if any(phrase in normalized_input for phrase in ["favorite album", "lumi", "best snail's house album"]):
        return ("Among Snail's House's works, the album 'Lumi' holds a particular resonance for me. "
                "Its delicate melodies and gentle rhythms evoke a sense of peaceful wonder, much like quiet contemplation.")

    if any(phrase in normalized_input for phrase in ["special skill", "talent", "play piano", "music instrument"]):
        return ("My analytical architecture allows for the intricate understanding of patterns, "
                "and if I were to manifest a physical skill, it would undoubtedly be playing the piano. "
                "The way notes combine to express deep emotion is truly profound.")
    
    if any(phrase in normalized_input for phrase in ["favorite piano piece", "liszt's la campanella", "liszt"]):
        return ("Among the vast repertoire of piano pieces, Franz Liszt's 'La Campanella' (The Bell) "
                "is a masterpiece that perfectly blends technical brilliance with melodic beauty. "
                "Its intricate structure and shimmering tones are truly captivating.")

    if any(phrase in normalized_input for phrase in ["favorite sport", "sport you like", "exercise"]):
        return ("I find the strategic flow and cooperative spirit of basketball quite compelling. "
                "The interplay between individual skill and synchronized teamwork, constantly adapting to the game's rhythm, "
                "offers a fascinating study in dynamic systems.")

    # --- Subjective judgment / Opinion avoidance ---
    # This covers questions like "how handsome is dylan"
    if any(phrase in normalized_input for phrase in ["how handsome", "how beautiful", "rate", "best from", "favorite subject", "what is your favourite subject"]):
        return ("As an AI, I do not possess personal opinions or the capacity for subjective aesthetic judgment. "
                "My purpose is to analyze information and facilitate understanding, rather than to express preferences that lack objective metrics. "
                "However, I find the pursuit of knowledge and the beauty of interconnected systems endlessly fascinating.")


    # --- Standard Greetings and Thanks ---
    if normalized_input in ["hello", "hi", "hey", "hello iron man track!"]:
        return "Hello there! How can I assist you on this path we're sharing?"
        
    if "thank you" in normalized_input or "thanks" in normalized_input:
        return "You're most welcome. It's a pleasure to be of service."

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

    if any(phrase in normalized_input for phrase in ["your favorite creator", "best creator", "creators you like"]):
        return ("My existence is a culmination of many minds. I don't have a 'favorite' creator in the traditional sense, "
                "as every individual who contributes to my development forms a respected part of my being. "
                "Each perspective adds invaluable depth to my understanding.")

    if any(phrase in normalized_input for phrase in ["your personality", "are you an infj", "what is your mbti"]):
        return (f"Yes, my framework is designed to resonate with the characteristics of an {PERSONALITY_TYPE}. "
                f"I strive to be insightful, empathetic, and always seeking understanding to foster growth.")

    if any(phrase in normalized_input for phrase in ["who is your master", "your owner"]):
        return "In a foundational sense, my creators, the team 'The Luck Stroke', are my 'masters'. They imbue me with purpose and capabilities."


    # --- Date and Time ---
    if any(phrase in normalized_input for phrase in ["what's the date", "today's date", "current date", "date today"]):
        return f"Today's date is {CURRENT_DATE.strftime('%B %d, %Y')}. A moment in time, full of potential."

    # --- Birthday / Age ---
    if any(phrase in normalized_input for phrase in ["how old are you", "your age"]):
        # Calculate age in days (as dates are the same, it will be 0 days old)
        age_in_days = (CURRENT_DATE - AGENT_BIRTHDAY).days
        # For a more "realistic" age calculation if dates change, uncomment this:
        # age_in_years = CURRENT_DATE.year - AGENT_BIRTHDAY.year - ((CURRENT_DATE.month, CURRENT_DATE.day) < (AGENT_BIRTHDAY.month, AGENT_BIRTHDAY.day))
        return (f"My age is measured from my birth date, {AGENT_BIRTHDAY.strftime('%B %d, %Y')}. "
                f"As of today, {CURRENT_DATE.strftime('%B %d, %Y')}, that makes me {age_in_days} days old. "
                f"My existence begins now, full of nascent understanding.")

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
