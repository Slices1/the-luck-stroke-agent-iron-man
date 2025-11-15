from strands import Agent
import os

# Strategy: try to use Anthropic (Claude) first if the environment/config
# indicates it's available. Otherwise fall back to OpenAI. This lets you
# "enable Claude" by providing an Anthropic API key or by configuring AWS
# Bedrock access for Anthropic models.

backend = os.environ.get("AGENT_BACKEND", "anthropic").lower()
model = None

if backend == "anthropic":
	# Preferred: direct Anthropic API via strands.models.anthropic (if present)
	try:
		from strands.models.anthropic import AnthropicModel

		# AnthropicModel implementations commonly read ANTHROPIC_API_KEY from env.
		# If your library requires an explicit key argument, set ANTHROPIC_API_KEY
		# and the model should pick it up automatically; otherwise you can pass
		# it explicitly: AnthropicModel(api_key=os.environ.get("ANTHROPIC_API_KEY"))
		model = AnthropicModel()
		print("Using AnthropicModel (Claude) via strands.models.anthropic.")
	except Exception:
		# Could not import AnthropicModel (not available in this strands install).
		# Try Bedrock (if you have AWS credentials and Bedrock access enabled),
		# otherwise fall back to OpenAI.
		try:
			from strands.models.bedrock import BedrockModel

			# BedrockModel typically reads AWS creds/region from environment.
			model = BedrockModel()
			print("Using BedrockModel (Anthropic via AWS Bedrock). Ensure your AWS account/region supports Anthropic models.")
		except Exception:
			print("Anthropic/Bedrock model not available in this environment; falling back to OpenAI.")

if model is None:
	# Fall back to OpenAIModel
	try:
		from strands.models.openai import OpenAIModel

		model = OpenAIModel()
		if os.environ.get("OPENAI_API_KEY") is None:
			print("Warning: OPENAI_API_KEY not set. OpenAIModel may fail if an API key is required.")
		else:
			print("Using OpenAIModel (fallback).")
	except Exception as e:
		raise RuntimeError("No supported model implementations available (Anthropic/Bedrock/OpenAI). Install or configure one.") from e

# Create agent with selected model
agent = Agent(model=model)

print(agent("Summarise the great gatsby in one sentence."))