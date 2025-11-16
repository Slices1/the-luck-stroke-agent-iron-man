from strands import Agent
from strands.models.openai import OpenAIModel

agent = Agent()
agent("")
print(agent("Summarise the great gatsby in one sentence."))