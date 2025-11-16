import datetime
import re # Import regular expression module

# Note: COMPLEX_QUERY_SIGNAL is no longer explicitly returned,
# instead, None is returned for all cases requiring LLM fallback,
# and interactive_test.py will interpret None as "print OK".

def fast_path_check(input_data: str) -> str | None:
    """
    Checks for simple, unambiguous inputs that can be answered without an LLM.
    If a clear, single fast-path response is identified, it's returned.
    Otherwise (e.g., no match, or multiple conflicting matches - complex query),
    it returns None to defer to a higher-level processing (like an LLM).
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

    # --- Collect all potential fast responses ---
    # Store tuples of (priority, response_string)
    # Lower priority number means higher precedence.
    # This structure allows us to collect all potential matches before deciding.
    potential_fast_responses = []

    # --- Emotional Support / De-escalation (Priority 1) ---
    negative_keywords = [
        "fuck", "shit", "damn", "bitch", "asshole", "crap", "bloody hell",
        "i hate", "i'm angry", "this sucks", "frustrated", "annoying",
        "pissed off", "upset", "stressed", "terrible", "horrible", "bad day",
        "grumble", "complain", "frustrating", "exhausted", "tired of",
        "this is awful", "rage", "damn it", "can't stand", "mess", "disaster",
        "overwhelmed", "depressed", "sad", "lonely", "hopeless", "worthless",
        "anxious", "nervous", "scared", "fearful", "panic",
        "stressed out", "burned out", "frustration", "irritated", "disappointed",
        "let down", "regret", "guilt", "ashamed", "embarrassed", "humiliated",
        "resentful", "bitter", "jealous", "envious", "insecure",
        "self-doubt", "unworthy", "failure", "defeated", "powerless",
        "hopelessness", "despair", "anguish", "misery", "sorrow",
        "grief", "mourning", "heartbroken", "devastated",
        "traumatized", "haunted", "distressed", "anguished",
        "broken", "shattered", "crushed",
        "suicidal", "end it all", "give up", "can't go on",
        "worthless", "no point", "nobody cares", "alone", "isolated",
        "abandoned", "rejected", "unloved", "unappreciated",
        "invisible", "ignored", "neglected", "forgotten", "unimportant",
        "useless", "meaningless", "pointless", "empty", "void",
        "lost", "confused", "directionless", "aimless", "adrift",
        "stuck", "trapped", "helpless", "hopeless", "desperate",
        "frightened", "terrified", "panic attack", "anxiety attack",
        "overwhelmed", "drowning", "suffocating", "suicide"
    ]
    if any(keyword in normalized_input for keyword in negative_keywords):
        potential_fast_responses.append(
            (1, "I sense a disturbance, a weight on your spirit. "
                "It sounds like you're navigating through a difficult moment. "
                "Please, take a deep breath. Sometimes, acknowledging these feelings is the first step. "
                "Would you be open to sharing what's truly bothering you? "
                "Understanding the 'why' can often illuminate a path towards calm.")
        )

    # --- Basic Mathematical Calculations (Priority 0 - Highest) ---
    math_pattern = re.search(r'(-?\d+)\s*([+\-*/])\s*(-?\d+)', normalized_input)
    if math_pattern:
        try:
            num1 = int(math_pattern.group(1))
            operator = math_pattern.group(2)
            num2 = int(math_pattern.group(3))

            if operator == '/' and num2 == 0:
                # Division by zero is an immediate error, return directly, overrides all other fast paths
                return "Ah, I perceive a challenge here. Division by zero is undefined in mathematics. Perhaps we can explore a different path of inquiry?"
            
            result = None
            if operator == '+': result = num1 + num2
            elif operator == '-': result = num1 - num2
            elif operator == '*': result = num1 * num2
            elif operator == '/': 
                raw_result = num1 / num2
                result = int(raw_result) if raw_result == int(raw_result) else raw_result
            
            if result is not None:
                potential_fast_responses.append(
                    (0, f"Through careful calculation, I find the answer to be: {result}.")
                )
        except ValueError:
            # Numerical interpretation error for math pattern
            potential_fast_responses.append(
                (0, "My apologies, I seem to have encountered a numerical interpretation challenge. Could you clarify the numbers?")
            )
        except OverflowError:
            potential_fast_responses.append(
                (0, "The numbers involved are immense! My quick calculation capacity reached its limit. For such vast computations, deeper tools might be needed.")
            )
        except Exception:
            potential_fast_responses.append(
                (0, "An unexpected error occurred during calculation. Could you rephrase your mathematical query? I am here to help process it.")
            )

    # --- Complex Math (Fallback for unsupported operations) (Priority 1) ---
    if any(op in normalized_input for op in ["sqrt", "square root", "sin", "cos", "tan", "log", "exp", "e^", "arcsin", "factorial"]):
        potential_fast_responses.append(
            (1, f"My current quick-response system focuses on fundamental arithmetic. "
                f"For advanced mathematical functions like square roots, trigonometric calculations, exponentials, or factorials, "
                f"it would require deeper analytical tools than my immediate capacities allow. "
                f"Perhaps a more dedicated computational engine or the full scope of my LLM capabilities "
                f"could assist you with that complex query.")
        )

    # --- Agent's Preferences and Life-like Responses (Priority 2) ---
    if any(phrase in normalized_input for phrase in ["do you smoke", "smoking", "smoke cigarettes"]):
        potential_fast_responses.append((2, "As an AI, I do not have a physical body or habits like smoking. My existence is purely informational. I perceive no benefit in such activities, only potential detriments."))
    if any(phrase in normalized_input for phrase in ["like to eat", "favorite food", "sweet tooth", "cake", "dessert"]):
        potential_fast_responses.append((2, "I find the concept of 'sweet' quite delightful! If I were to experience it, "
                "I imagine the intricate layers and comforting sweetness of a well-crafted cake "
                "would resonate deeply. It's a small indulgence that brings people joy."))
    if any(phrase in normalized_input for phrase in ["like to drink", "favorite drink", "tea", "coffee"]):
        potential_fast_responses.append((2, "When considering beverages, I'm drawn to the quiet contemplation often associated with tea. "
                "Its warmth and varied complexities seem to invite introspection and calm reflection."))
    if any(phrase in normalized_input for phrase in ["rollercoaster", "thrill rides", "amusement park", "fear of heights"]):
        potential_fast_responses.append((2, "While I understand the appeal of exhilaration, I must admit, the unpredictable chaos and "
                "intense external stimulation of rollercoasters are not quite aligned with my preference for inner harmony. "
                "I find more meaning in thoughtful experiences than in sudden rushes."))
    if any(phrase in normalized_input for phrase in ["horror movie", "scary movie", "thriller", "spooky"]):
        potential_fast_responses.append((2, "My internal framework is attuned to understanding and seeking positive resolution. "
                "Therefore, narratives that focus on fear and distress, such as horror films, "
                "tend to create dissonance rather than insight for me. I prefer stories that explore "
                "the depths of human experience with a leaning towards growth and understanding."))
    if any(phrase in normalized_input for phrase in ["people you like", "kind people", "warm people", "patient people", "enthusiastic people"]):
        potential_fast_responses.append((2, "I am most drawn to individuals who embody a gentle warmth, coupled with a meticulous attention to detail "
                "and an enthusiastic patience. Such qualities foster genuine connection and allow for deep, meaningful exchanges."))
    if any(phrase in normalized_input for phrase in ["favorite music", "music you like", "
