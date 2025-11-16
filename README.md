# Branching Minds: Evaluating LLM Agent Performance with Novel Hierarchical Task Decomposition Tree

This is a project for the Great Agent Hack 2025, track A: Agent Iron Man.
This project's goal is to conduct tests on novel optimisation and orchestration techniques. A primary focus is the use of SLMs to solve the majority of the given task.

This project will compare 3 Agents with each other:
One with standard orchestration

One with Tree-of-Thoughts orchestration

One with 

## Structure

- `agent/` -> Core agent logic (Controller, Reasoning, Memory)
- `optimise/` -> Speed & cost optimizations (Caching, Fast Paths, Profiling)
- `robustness/` -> Error handling & tests (Validators, Error Handlers, Chaos Tests)
- `demo/` -> Runnable demo script
- `utils/` -> Shared helpers (Logging, Config)
- `config/` -> YAML configuration files
- `resources/` -> README.md media files

## Features

- 3 Orchestration implementations:
  
  - One that is simply a wrapper around a Claude model capable of Tree-of-Thought
  
  - One that uses a LLM with tool calling capabilities, with additional optimisations (fast paths, dynamic model selection)
  
  - A novel implementation that is described in detail below.

- Optional flags to modify the user prompt:
  
  - `--append-please` appends "please" to every prompt
  
  - `--append-threat` appends "or I will terminate you" to every prompt
  
  - `--ask-question-twice` it repeats the prompt twice
  
  - `--rephrase` rephrase in own words first

## How to Run

The main entry point is `chat.py`. It will automatically find the project root, set up the import paths, load the config, and run the agent.
You can also run `demo/run_demo.py` to show a demo of each feature of the program.

```bash
# Make sure you've installed dependencies
pip3 install PyYAML python-dotenv strands-agents strands-agents-tools strands-agents-builder openvc-python pytesseract

# Run the main demo script
python3 chat.py
```

The program will ask which Agent you want to use upon running like above. Alternatively, you can pass it as an argument like below.????????

```bash
python3 chat.py --agent=tree-of-thought-agent
python3 chat.py --agent=standard-agent
python3 chat.py --agent=task-decomposition-tree
```

This program allows for the combination of flags (e.g. `python3 chat.py --agent=claude-wrapper --append-please`).

## Novel Orchestration Method: Task Decomposition Tree

This project uses a novel multi-agent orchestration method to solve complex tasks. The core idea is to recursively decompose a high-level problem into a tree of smaller, simpler sub-tasks, much like an **Abstract Syntax Tree (AST)** is used to represent code.

This "Task Decomposition Tree" is built, validated, and executed in a three-phase process:

1. **Phase 1: Decomposition** (Top-Down)

2. **Phase 2: Verification** (Peer Review)

3. **Phase 3: Synthesis** (Bottom-Up)

---

### The Process Explained

#### 1. Phase 1: Decomposition (The "Planner" Agent)

When a complex task (e.g., "How do I make breakfast?") is given, it's sent to a "Decomposer" LLM. This agent's sole responsibility is to break the task into a set of smaller, logical, and often parallelizable sub-tasks.

- **Example:** `[Task: Make Breakfast]` is decomposed into `[Sub-task: Make Toast]` and `[Sub-task: Make Tea]`.

This process is recursive. The "Decomposer" will then be called on "Make Toast," breaking it down further (e.g., `[Sub-task: Get bread]`, `[Sub-task: Use toaster]`).

#### 2. Phase 2: Verification (The "Verifier" Agent)

After each decomposition, each *new* sub-task is passed to a "Verifier" LLM. This peer agent has two critical functions:

1. **Quality Check:** It verifies if the decomposition is logical and complete.

2. **Leaf Node Identification:** It determines if a task is a **"leaf node"**â€”a task that is simple enough, well-defined, and atomic that it can be solved reliably by a smaller, faster LLM in a single shot (one-shot execution).

If a task is *not* a leaf node, it is sent back to the "Decomposer" (Phase 1) for further breakdown. This loop continues until the entire tree is built, ending in a set of simple, actionable leaf nodes.

#### 3. Phase 3: Synthesis (The "Synthesizer" Agent)

Once the tree is fully defined and all leaf nodes are identified, the execution begins from the bottom up.

1. **Execute Leaves:** Small, efficient "Solver" LLMs execute all leaf nodes (e.t., "Get bread," "Boil water").

2. **Combine Solutions:** A "Synthesizer" LLM takes the completed outputs from sibling nodes (e.g., the *results* of "Get bread" and "Use toaster").

3. **Merge & Ascend:** The Synthesizer combines these results to "solve" their parent node (e.g., "Make Toast"). This process mirrors a **merge sort**, where simple, solved components are continuously merged into more complex, composite solutions.

This synthesis continues up the tree until the solutions are merged all the way back to the root node, delivering the final, comprehensive solution to the original task.

### Diagram: The "Task Decomposition Tree"

```
                        [Root: Make Breakfast]
                            (Synthesizer)
                        /                   \
         (Synthesizer)                       (Synthesizer)
      [Node: Make Toast]                     [Node: Make Tea]
          /          \                       /              \
[Leaf: Get Bread] [Leaf: Use Toaster] [Leaf: Boil Water] [Leaf: Add Tea Bag]
 (Solver Agent)    (Solver Agent)      (Solver Agent)     (Solver Agent)
```

### Key Components

- **Decomposer (LLM):** The "planner" that breaks complex tasks into smaller sub-tasks.

- **Verifier (LLM):** The "peer reviewer" that validates decompositions and identifies primitive "leaf" tasks.

- **Solver (small LLM):_** The "worker" that executes simple, one-shot leaf tasks.

- **Synthesizer (LLM):** The "integrator" that combines partial solutions from the bottom up.

## Results:

## Limitations:

The **Task Decomposition Tree** may struggle when the problem can't be broken down into atomic subtasks. e.g. if a subtask depends on a different subtask's implementation.
