import unittest
import sys
import os

# --- CRITICAL IMPORT FIX for testing ---
script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.insert(0, project_root)
# ---------------------------------------

from agent.controller import AgentController
from utils.config_loader import load_config
from robustness.chaos_tests import chaos_tool_executor

class TestAgentRobustness(unittest.TestCase):

    def setUp(self):
        """Set up a fresh agent for each test."""
        config = load_config()
        self.agent = AgentController(config)

    def test_01_fast_path_works(self):
        """Tests that the optimisation team's fast path is triggered."""
        print("\n[Test] Running test_01_fast_path_works...")
        test_input = "hello"
        expected_output = "Fast path response: Hello! How can I help you today?"
        result = self.agent.run_step(test_input)
        self.assertEqual(result, expected_output)
        print("...Passed")

    def test_02_invalid_input_is_handled(self):
        """Tests that the robustness team's validator is triggered."""
        print("\n[Test] Running test_02_invalid_input_is_handled...")
        test_input = "" # Empty string is invalid
        expected_output = "Error: Input was invalid. Please rephrase. (Received: '')"
        result = self.agent.run_step(test_input)
        self.assertEqual(result, expected_output)
        print("...Passed")

    def test_03_tool_failure_is_handled(self):
        """Tests that the robustness team's error handler catches a tool crash."""
        print("\n[Test] Running test_03_tool_failure_is_handled...")
        
        # Force a failure by re-assigning the executor to one that raises an error
        def failing_tool(plan):
            raise ValueError("Test Failure")
        
        self.agent.tool_executor = failing_tool
        
        test_input = "This will fail the tool"
        result = self.agent.run_step(test_input)
        self.assertIn("Error: The agent's tool failed.", result)
        print("...Passed")

if __name__ == "__main__":
    unittest.main()
