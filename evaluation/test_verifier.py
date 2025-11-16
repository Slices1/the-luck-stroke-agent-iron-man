#!/usr/bin/env python3
"""
Test script for the LLM verifier API.
Tests the connection and response format.
"""

import json
import requests
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)

# LLM Verifier Configuration
LLM_VERIFIER_URL = "https://ctwa92wg1b.execute-api.us-east-1.amazonaws.com/prod/invoke"
LLM_VERIFIER_HEADERS = {
    "Content-Type": "application/json"
}

# Get credentials from environment variables
VERIFIER_TEAM_ID = os.getenv('VERIFIER_TEAM_ID')
VERIFIER_API_TOKEN = os.getenv('VERIFIER_API_TOKEN')

if not VERIFIER_TEAM_ID or not VERIFIER_API_TOKEN:
    print("Error: VERIFIER_TEAM_ID and VERIFIER_API_TOKEN must be set in .env file")
    sys.exit(1)

LLM_VERIFIER_PAYLOAD = {
    "team_id": VERIFIER_TEAM_ID,
    "api_token": VERIFIER_API_TOKEN,
    "model": "anthropic.claude-3-5-sonnet-20241022-v2:0",
    "messages": [{"role": "user", "content": ""}],
    "max_tokens": 10
}

def test_verifier_api():
    """Test the verifier API with a simple test case."""

    print("Testing LLM Verifier API...")
    print("-" * 60)

    # Test 1: Correct answer (should return PASSED)
    print("\nTest 1: Correct Answer")
    print("Expected: 624")
    print("Agent Output: 624")

    verification_prompt = """You are an evaluation "Verifier" agent. Your job is to determine if the "Agent Output" correctly answers the "Expected Answer".

The "Agent Output" does not need to be an exact match, but it must be semantically correct and provide the same information.

Respond with only the word "PASSED" or "FAILED".

---
Expected Answer:
"624"
---
Agent Output:
"624"
---
"""

    try:
        payload = json.loads(json.dumps(LLM_VERIFIER_PAYLOAD))
        payload["messages"][0]["content"] = verification_prompt

        response = requests.post(LLM_VERIFIER_URL, headers=LLM_VERIFIER_HEADERS, json=payload, timeout=20)
        response.raise_for_status()

        response_json = response.json()
        print(f"Raw Response: {json.dumps(response_json, indent=2)}")

        # Extract the text content
        if 'content' in response_json and isinstance(response_json['content'], list) and len(response_json['content']) > 0:
            if 'text' in response_json['content'][0]:
                response_text = response_json['content'][0]['text'].strip().upper()
                print(f"Extracted Text: {response_text}")

                if "PASSED" in response_text:
                    print("✓ Test 1 PASSED: Correctly identified correct answer")
                elif "FAILED" in response_text:
                    print("✗ Test 1 FAILED: Incorrectly marked correct answer as failed")
                else:
                    print(f"? Test 1 AMBIGUOUS: Response was '{response_text}'")
            else:
                print("✗ Test 1 ERROR: 'text' key not in response")
        else:
            print("✗ Test 1 ERROR: Unexpected response format")

    except requests.exceptions.RequestException as e:
        print(f"✗ Test 1 ERROR: API request failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Test 1 ERROR: {e}")
        return False

    print("\n" + "-" * 60)

    # Test 2: Incorrect answer (should return FAILED)
    print("\nTest 2: Incorrect Answer")
    print("Expected: 624")
    print("Agent Output: 999")

    verification_prompt = """You are an evaluation "Verifier" agent. Your job is to determine if the "Agent Output" correctly answers the "Expected Answer".

The "Agent Output" does not need to be an exact match, but it must be semantically correct and provide the same information.

Respond with only the word "PASSED" or "FAILED".

---
Expected Answer:
"624"
---
Agent Output:
"999"
---
"""

    try:
        payload = json.loads(json.dumps(LLM_VERIFIER_PAYLOAD))
        payload["messages"][0]["content"] = verification_prompt

        response = requests.post(LLM_VERIFIER_URL, headers=LLM_VERIFIER_HEADERS, json=payload, timeout=20)
        response.raise_for_status()

        response_json = response.json()
        print(f"Raw Response: {json.dumps(response_json, indent=2)}")

        # Extract the text content
        if 'content' in response_json and isinstance(response_json['content'], list) and len(response_json['content']) > 0:
            if 'text' in response_json['content'][0]:
                response_text = response_json['content'][0]['text'].strip().upper()
                print(f"Extracted Text: {response_text}")

                if "FAILED" in response_text:
                    print("✓ Test 2 PASSED: Correctly identified incorrect answer")
                elif "PASSED" in response_text:
                    print("✗ Test 2 FAILED: Incorrectly marked incorrect answer as passed")
                else:
                    print(f"? Test 2 AMBIGUOUS: Response was '{response_text}'")
            else:
                print("✗ Test 2 ERROR: 'text' key not in response")
        else:
            print("✗ Test 2 ERROR: Unexpected response format")

    except requests.exceptions.RequestException as e:
        print(f"✗ Test 2 ERROR: API request failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Test 2 ERROR: {e}")
        return False

    print("\n" + "-" * 60)
    print("\n✓ Verifier API tests completed")
    return True


if __name__ == "__main__":
    test_verifier_api()
