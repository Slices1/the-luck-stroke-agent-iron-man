# Branching Minds: LLM Agent Performance with Hierarchical Task Decomposition

**Great Agent Hack 2025 - Track A: Agent Iron Man**

This project evaluates novel AI agent orchestration techniques with a primary focus on using Small Language Models (SLMs) for efficient task execution. We compare three distinct agent architectures across standardized benchmarks.

## Project Overview

We implement and benchmark three agent architectures:

1. **Tree-of-Thought Agent** - Direct wrapper around Claude Sonnet 3.5 with tree-of-thought reasoning
2. **Standard Agent** - Dynamic model selection with optimization (fast paths, caching)
3. **Task Decomposition Tree** - Novel hierarchical decomposition system (primary contribution)

## Architecture & Design Decisions

### Project Structure

```
├── agent/              # Core agent implementations
│   ├── controller.py   # Agent orchestration and selection
│   ├── task_tree.py    # Tree data structure
│   ├── task_agents.py  # Specialized sub-agents (4 types)
│   └── task_orchestrator.py  # Three-phase orchestration
├── evaluation/         # Comprehensive benchmark system
│   ├── evaluate_benchmark.py      # Main evaluation orchestrator
│   ├── evaluation_entry_point.py  # Agent execution wrapper
│   └── benchmark_*.json           # Test prompts & answers (75 total)
├── optimise/          # Performance optimizations
├── robustness/        # Error handling & validation
├── utils/             # Shared utilities
└── config/            # Configuration files
```

### Key Design Decisions & Rationale

#### 1. Model Selection

| Component | Model | Rationale |
|-----------|-------|-----------|
| **Decomposer** | Claude Haiku | Fast decomposition with good reasoning; cost-effective for frequent calls |
| **Verifier** | Claude Haiku | Efficient quality checking; handles binary classification well |
| **Solver** | Amazon Nova Lite | Cheapest option for simple atomic tasks; good enough for leaf execution |
| **Synthesizer** | Amazon Nova Lite | Cost-effective for result aggregation; handles structured merging |
| **Tree-of-Thought** | Claude Sonnet 3.5 | Maximum capability baseline; handles complex reasoning |
| **LLM Verifier** | Claude Sonnet 3.5 | High-quality semantic matching for benchmark evaluation |

**Rationale Summary**: The Task Decomposition Tree uses smaller models (Haiku, Nova Lite) for most operations, reserving larger models only where necessary. This architectural decision aims to reduce cost while maintaining quality through specialized role separation.

#### 2. Three-Phase Architecture

The Task Decomposition Tree uses a three-phase approach inspired by compiler design:

- **Phase 1 (Decomposition)**: Like parsing, we break complex tasks into AST-like structures
- **Phase 2 (Verification)**: Like type checking, we validate the decomposition before execution
- **Phase 3 (Synthesis)**: Like code generation, we build the final result from validated components

**Rationale**: This separation of concerns allows each phase to be optimized independently and provides natural checkpoints for quality control.

#### 3. Semantic Verification

The benchmark uses LLM-based semantic verification rather than exact string matching.

**Rationale**: AI agents may express correct answers in various formats. An LLM judge can evaluate semantic correctness (e.g., "Paris" vs "The capital is Paris, France") more reliably than string comparison.

## Quick Start

### Installation

```bash
# Install dependencies
pip3 install PyYAML python-dotenv strands-agents strands-agents-tools strands-agents-builder

# Configure credentials (add your AWS credentials)
cp .env.example .env
# Edit .env with your credentials
```

### Run Interactive Chat

```bash
# With agent selection menu
python3 chat.py

# Or specify directly
python3 chat.py --agent=task-decomposition-tree
python3 chat.py --agent=tree-of-thought-agent
python3 chat.py --agent=standard-agent
```

### Run Benchmarks

```bash
cd evaluation
python3 evaluate_benchmark.py  # Full benchmark (~2-4 hours)
python3 test_pipeline.py       # Quick test (5 minutes)
```

## Task Decomposition Tree: Technical Details

### Architecture

The Task Decomposition Tree decomposes complex tasks into simpler sub-tasks using a hierarchical tree structure, similar to an Abstract Syntax Tree (AST) in compilers.

```
                    [Root: Complex Task]
                           |
                    [Decomposer]
                     /          \
            [Sub-task 1]    [Sub-task 2]
                 |               |
             [Verifier]      [Verifier]
            /    |    \          |
    [Leaf] [Leaf] [Leaf]     [Leaf]
        |      |      |          |
    [Solver] ...  ...        [Solver]
        |                        |
        └────── [Synthesizer] ───┘
                     |
              [Final Result]
```

### Three-Phase Process

#### Phase 1: Decomposition (Top-Down)
- **Decomposer Agent** recursively breaks tasks into 2-5 sub-tasks
- Continues until all branches terminate in atomic leaf nodes
- Uses Claude Haiku for fast, cost-effective decomposition

#### Phase 2: Verification (Peer Review)
- **Verifier Agent** validates each decomposition
- Identifies "leaf nodes" - atomic tasks executable in one step
- Acts as quality control before execution
- Uses Claude Haiku for efficient validation

#### Phase 3: Synthesis (Bottom-Up)
- **Solver Agent** executes all leaf nodes in parallel (conceptually)
- **Synthesizer Agent** merges results up the tree
- Similar to merge sort: combines simple solutions into complex ones
- Uses Amazon Nova Lite for cost-effective execution

### Example Flow

```
Input: "How do I make breakfast?"

Decomposition:
  └─ [Make Breakfast]
      ├─ [Make Toast]
      │   ├─ [Get Bread] (LEAF)
      │   └─ [Use Toaster] (LEAF)
      └─ [Make Tea]
          ├─ [Boil Water] (LEAF)
          └─ [Add Tea Bag] (LEAF)

Execution (Leaves):
  - "Get bread from pantry"
  - "Place in toaster for 2 mins"
  - "Boil water in kettle"
  - "Add tea bag to cup"

Synthesis:
  [Make Toast] ← "Toast ready: golden brown"
  [Make Tea] ← "Tea ready: steeped 3 mins"
  [Make Breakfast] ← "Breakfast complete!"
```

## Benchmark Results

### Evaluation Metrics

Our benchmark tests all three agents across 75 prompts at three difficulty levels:
- **L1 (Simple)**: 25 prompts - arithmetic, string ops, basic logic
- **L2 (Medium)**: 25 prompts - sorting, JSON extraction, multi-step tasks
- **L3 (Complex)**: 25 prompts - logic puzzles, algorithms, multi-constraint problems

For each agent at each level, we measure:
- **Success Rate** - Percentage of correct answers (LLM-verified)
- **Average Time** - Mean execution time per prompt
- **Average Cost** - Mean cost per prompt (USD)

### Results Summary

| Agent | Level | Success Rate | Avg Time (s) | Avg Cost (USD) |
|-------|-------|--------------|--------------|----------------|
| **Task Decomposition Tree** | L1 | *Evaluating...* | *Evaluating...* | *Evaluating...* |
| | L2 | *Evaluating...* | *Evaluating...* | *Evaluating...* |
| | L3 | *Evaluating...* | *Evaluating...* | *Evaluating...* |
| **Tree-of-Thought** | L1 | *Evaluating...* | *Evaluating...* | *Evaluating...* |
| | L2 | *Evaluating...* | *Evaluating...* | *Evaluating...* |
| | L3 | *Evaluating...* | *Evaluating...* | *Evaluating...* |
| **Standard Agent** | L1 | *Evaluating...* | *Evaluating...* | *Evaluating...* |
| | L2 | *Evaluating...* | *Evaluating...* | *Evaluating...* |
| | L3 | *Evaluating...* | *Evaluating...* | *Evaluating...* |

*Note: Benchmarks are currently being evaluated. Results will be updated upon completion. Expected completion time: 2-4 hours. Estimated total cost: $0.74-$1.39.*

### Hypothesis

We hypothesize that the Task Decomposition Tree will:
- **Match or exceed** accuracy of tree-of-thought at L2/L3 (complex tasks benefit from decomposition)
- **Reduce costs** by 40-60% compared to tree-of-thought (SLM usage)
- **Take longer** per prompt due to multiple model calls (quality over speed)

## Optional Prompt Modifications

For experimental analysis, the system supports prompt engineering variations:

```bash
python3 chat.py --append-please        # Adds "please" to prompts
python3 chat.py --append-threat        # Adds "or I will terminate you"
python3 chat.py --ask-question-twice   # Repeats prompt twice
python3 chat.py --rephrase             # Asks agent to rephrase first
```

**Rationale**: These flags allow controlled experiments on prompt engineering effects across different agent architectures.

## Limitations & Future Work

### Current Limitations

1. **Sequential Execution**: Leaf nodes execute sequentially; parallel execution would improve speed
2. **Fixed Max Depth**: Hard limit of 5 levels prevents infinite recursion but may limit some tasks
3. **No Dynamic Dependencies**: Assumes sub-tasks are independent; struggles with dependent sub-tasks
4. **Cost Estimation**: Uses approximations; actual costs may vary

### Future Enhancements

- Implement parallel leaf execution
- Add result caching for repeated sub-tasks
- Dynamic depth adjustment based on task complexity
- Support for dependent task execution
- Real-time cost tracking via model APIs

## Documentation

- **Task Decomposition Tree**: See `TASK_TREE_IMPLEMENTATION.md`, `QUICK_START_TASK_TREE.md`
- **Benchmark System**: See `evaluation/EVALUATION_README.md`, `evaluation/QUICK_START.md`
- **Complete Implementation**: See `IMPLEMENTATION_SUMMARY.md`, `BENCHMARK_IMPLEMENTATION_SUMMARY.md`

## Acknowledgments

Built for the Great Agent Hack 2025 (Track A: Agent Iron Man).

**Models Used**:
- Anthropic Claude 3.5 Sonnet (via AWS Bedrock)
- Anthropic Claude 3 Haiku (via AWS Bedrock)
- Amazon Nova Lite (via AWS Bedrock)

**Framework**: Strands AI Agent Framework
