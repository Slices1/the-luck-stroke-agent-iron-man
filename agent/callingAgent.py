from strands import Agent
from strands_tools import calculator, speak, use_computer
import os
from dotenv import load_dotenv

# os.environ["AWS_ENDPOINT_URL"] = api_endpoint
load_dotenv() # Load environment variables from .env file
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")

agent = Agent(tools=[calculator, speak, use_computer])

def prompting():
    while True:
        prompt = input("User> ")
        agent(prompt)

print()
# To run this script, ensure you have a .env file in the same directory with the following content:
# AWS_ACCESS_KEY_ID=your-access-key-id
# AWS_SECRET_ACCESS_KEY=your-secret-access-key
# AWS_SESSION_TOKEN=your-session-token
# Replace 'your-access-key-id', 'your-secret-access-key', and 'your-session-token' with your actual AWS credentials.
# Then execute the script using Python 3.10 or higher.
# Also this while loop might be missing something i don't remember