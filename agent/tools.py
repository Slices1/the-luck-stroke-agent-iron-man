import logging
import time
import os

logger = logging.getLogger(__name__)

class LLMModel:
    """A dummy LLM model wrapper."""
    def __init__(self, model_name="stub-model"):
        self.model_name = model_name
        logger.info(f"LLMModel ({self.model_name}) initialized.")

    def query(self, prompt):
        """Simulates an LLM API call."""
        logger.debug(f"Querying model {self.model_name} with prompt: {prompt[:50]}...")
        time.sleep(0.1) # Simulate network latency
        return f"This is a dummy LLM response to '{prompt}'"


def get_preferred_model(config: dict = None):
    """Return a model-like object with a `query(prompt)` method.

    Prefer a Strands Agent backed by the OpenAIModel if available. Fall
    back to the local LLMModel stub.
    """
    cfg = config or {}
    try:
        # Try to import Strands and prefer GeminiModel when requested/available.
        from strands import Agent
        # Prefer Gemini model if present
        gemini_model_cls = None
        try:
            from strands.models.gemini import GeminiModel  # type: ignore
            gemini_model_cls = GeminiModel
        except Exception:
            gemini_model_cls = None

        if gemini_model_cls is not None and (cfg.get('PREFERRED_LLM', '').lower() in ('gemini', 'auto') or cfg.get('PREFERRED_LLM') is None):
            # Read credentials from config or environment. Do NOT hardcode secrets.
            team_id = cfg.get('GEMINI_TEAM_ID') or os.environ.get('GEMINI_TEAM_ID') or os.environ.get('STRANDS_GEMINI_TEAM_ID')
            api_token = cfg.get('GEMINI_API_TOKEN') or os.environ.get('GEMINI_API_TOKEN') or os.environ.get('STRANDS_GEMINI_API_TOKEN')
            try:
                if team_id and api_token:
                    model = gemini_model_cls(team_id=team_id, api_token=api_token)
                elif api_token:
                    # Some constructors may accept a single token param
                    model = gemini_model_cls(api_token=api_token)
                else:
                    model = gemini_model_cls()
            except TypeError:
                # Try alternate kwarg names
                try:
                    model = gemini_model_cls(token=api_token) if api_token else gemini_model_cls()
                except Exception:
                    model = gemini_model_cls()

            # Instantiate Agent with the Gemini model
            agent = Agent(model=model)
        else:
            # Fallback to OpenAIModel if Gemini not available or not preferred
            from strands.models.openai import OpenAIModel

            # Construct the OpenAIModel; many SDKs accept api_key or read env vars
            api_key = cfg.get('OPENAI_API_KEY') or os.environ.get('OPENAI_API_KEY')
            try:
                if api_key:
                    model = OpenAIModel(api_key=api_key)
                else:
                    model = OpenAIModel()
            except TypeError:
                # Some constructors may expect different kwarg names
                try:
                    model = OpenAIModel(token=api_key) if api_key else OpenAIModel()
                except Exception:
                    model = OpenAIModel()

            # Instantiate Agent with the model
            agent = Agent(model=model)

        # Return a thin wrapper exposing `query(prompt)` to match LLMModel
        class _Wrapper:
            def __init__(self, agent):
                self._agent = agent

            def query(self, prompt: str) -> str:
                # Try common agent call methods
                for method in ("run", "query", "generate", "respond", "__call__"):
                    fn = getattr(self._agent, method, None)
                    if callable(fn):
                        try:
                            return str(fn(prompt))
                        except TypeError:
                            try:
                                return str(fn(prompt=prompt))
                            except Exception:
                                continue
                # Fallback: try a generic call
                try:
                    return str(self._agent(prompt))
                except Exception as e:
                    raise RuntimeError(f"Strands agent failed to produce text: {e}")

        return _Wrapper(agent)
    except Exception:
        # If anything fails (Strands not installed or construction error) fall back
        # to the local stub which provides query().
        logger.info("Strands Agent unavailable or failed to initialize; using LLMModel stub")
        return LLMModel()

def execute_tool(plan: str):
    """
S    imulates executing a tool based on the agent's plan.
    """
    logger.info(f"Executing tool with plan: {plan}")
    
    # Simulate tool work
    time.sleep(0.2) # Simulate tool execution time
    
    if "fail" in plan.lower():
        # This allows the test_suite to trigger a failure
        raise ValueError("Tool execution failed as per plan.")
        
    tool_result = f"Tool successfully executed plan: '{plan}'"
    return tool_result


def add_numbers(a, b):
    """A small utility/tool that adds two numbers.

    Accepts numeric strings or numbers. Returns a tuple (sum, representation).
    The representation is a friendly string suitable for including in prompts.
    """
    logger.info(f"add_numbers called with: {a}, {b}")
    try:
        # Convert to float if contains a dot, otherwise int where possible
        def to_num(x):
            if isinstance(x, (int, float)):
                return x
            sx = str(x).strip()
            if '.' in sx:
                return float(sx)
            return int(sx)

        na = to_num(a)
        nb = to_num(b)
        result = na + nb
        # normalize int-like floats to int for nicer display
        if isinstance(result, float) and result.is_integer():
            result = int(result)

        rep = f"{na} + {nb} = {result}"
        logger.debug(f"add_numbers result: {rep}")
        return result, rep
    except Exception as e:
        logger.error(f"Failed to add numbers: {a}, {b} - {e}")
        raise
