# Iron Man Track Skeleton (Refactored)

This is the prototype for the Great Agent Hack 2025, Iron Man track.
This skeleton is fully integrated, and all modules are connected and testable.

## Structure

-   `agent/` -> Core agent logic (Controller, Reasoning, Memory)
-   `optimise/` -> Speed & cost optimizations (Caching, Fast Paths, Profiling)
-   `robustness/` -> Error handling & tests (Validators, Error Handlers, Chaos Tests)
-   `demo/` -> Main runnable script
-   `utils/` -> Shared helpers (Logging, Config)
-   `config/` -> YAML configuration files

## 🚀 How to Run

The main entry point is `demo/run_demo.py`. It will automatically find the project root, set up the import paths, load the config, and run the agent.

```bash
# Make sure you've installed dependencies
pip install PyYAML

# Run the main demo script
python3.11 demo/run_demo.py
```

## 🧪 How to Test

We use Python's built-in `unittest` library. You can run the entire test suite from the root directory:

```bash
# Run the robustness test suite
python -m unittest robustness/test_suite.py
