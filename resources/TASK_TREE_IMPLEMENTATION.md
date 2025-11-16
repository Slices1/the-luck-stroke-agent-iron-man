# Task Decomposition Tree - Implementation Guide

## Overview

The Task Decomposition Tree Agent is a novel multi-agent orchestration system that recursively decomposes complex tasks into simpler sub-tasks, executes them, and synthesizes results. This approach is inspired by Abstract Syntax Trees (ASTs) in compilers.

## Architecture

### Core Components

#### 1. **Data Structure** (`agent/task_tree.py`)

- `TaskNode`: Represents a single task in the tree
  - Tracks task description, status, parent/children relationships
  - Can be either a parent node or a leaf node
  - Stores results or errors after execution

- `TaskDecompositionTree`: Manages the complete tree structure
  - Provides tree traversal and node management
  - Tracks all nodes by ID
  - Calculates tree statistics (depth, leaf count, etc.)

#### 2. **Agents** (`agent/task_agents.py`)

Four specialized agents handle different aspects of the process:

##### DecomposerAgent (Phase 1)
- **Model**: `anthropic.claude-3-haiku-20240307-v1:0`
- **Purpose**: Break complex tasks into 2-5 smaller sub-tasks
- **Input**: Task description
- **Output**: List of sub-task descriptions (JSON array)

##### VerifierAgent (Phase 2)
- **Model**: `anthropic.claude-3-haiku-20240307-v1:0`
- **Purpose**:
  - Validate decompositions are logical and complete
  - Identify "leaf nodes" (atomic tasks)
- **Input**: Task description, optional parent context
- **Output**: Boolean (is_leaf / is_valid)

##### SolverAgent (Leaf Execution)
- **Model**: `us.amazon.nova-lite-v1:0`
- **Purpose**: Execute atomic leaf tasks
- **Input**: Simple task description
- **Output**: Task result/answer

##### SynthesizerAgent (Phase 3)
- **Model**: `us.amazon.nova-lite-v1:0`
- **Purpose**: Combine sub-task results into parent solutions
- **Input**: Parent task + list of sub-results
- **Output**: Synthesized result for parent task

#### 3. **Orchestrator** (`agent/task_orchestrator.py`)

The `TaskOrchestrator` coordinates the three-phase process:

1. **Phase 1 & 2: Tree Building** (Top-Down)
   - Recursively decomposes tasks using DecomposerAgent
   - Verifies each decomposition with VerifierAgent
   - Identifies leaf nodes
   - Continues until all branches end in leaves

2. **Phase 3: Execution & Synthesis** (Bottom-Up)
   - Executes all leaf nodes with SolverAgent
   - Synthesizes results up the tree with SynthesizerAgent
   - Returns final result at root node

#### 4. **Integration** (`agent/controller.py`)

The `TaskDecompositionTreeAgent` class integrates with the existing agent system:
- Implements the same interface as other agents
- Uses TaskOrchestrator internally
- Logs tree statistics after completion

## Three-Phase Process

### Phase 1: Decomposition (Top-Down)

```
[Root: Make Breakfast]
        |
        v (decompose)
    /-----------------\
[Make Toast]      [Make Tea]
    |                  |
    v (decompose)      v (decompose)
  /-------\          /----------\
[Get Bread] [Use   [Boil      [Add Tea
            Toaster] Water]     Bag]
```

- Start with root task
- DecomposerAgent breaks it into sub-tasks
- Recursively decompose each sub-task
- Continue until all branches end in leaf nodes

### Phase 2: Verification (Peer Review)

For each decomposition:
1. **Quality Check**: VerifierAgent validates the decomposition is logical
2. **Leaf Detection**: VerifierAgent determines if task is atomic

If a task is NOT a leaf, it goes back to Phase 1 for further decomposition.

### Phase 3: Synthesis (Bottom-Up)

```
[Get Bread]  --> "Got bread from pantry"
[Use Toaster] --> "Placed bread in toaster for 2 mins"
                        |
                        v (synthesize)
                [Make Toast] --> "Toast is ready: golden brown"

[Boil Water] --> "Water boiled in kettle"
[Add Tea Bag] --> "Tea bag added to cup"
                        |
                        v (synthesize)
                [Make Tea] --> "Tea is ready: steeped for 3 mins"

                        |
                        v (synthesize)
            [Make Breakfast] --> "Breakfast ready: toast and tea"
```

1. Execute all leaf nodes with SolverAgent
2. Synthesize sibling results with SynthesizerAgent
3. Continue merging up the tree
4. Return final result at root

## Usage

### Option 1: Via chat.py

```bash
python3 chat.py --agent=task-decomposition-tree
```

Then enter your task when prompted.

### Option 2: Direct Integration

```python
from agent.controller import TaskDecompositionTreeAgent

# Initialize the agent
agent = TaskDecompositionTreeAgent()

# Process a task
result = agent.run("How do I make breakfast?")
print(result)
```

### Option 3: Using the Orchestrator Directly

```python
from agent.task_orchestrator import TaskOrchestrator

# Initialize orchestrator
orchestrator = TaskOrchestrator()

# Process task
result = orchestrator.process_task("Explain photosynthesis")

# Get tree statistics
summary = orchestrator.get_tree_summary()
print(f"Nodes: {summary['total_nodes']}, Depth: {summary['depth']}")

# Print tree structure
orchestrator.tree.print_tree()
```

## Testing

### Run the test suite:

```bash
python3 test_task_tree.py
```

This runs three test cases:
1. Simple task (making tea)
2. Factual question (capital of France)
3. Complex task (water cycle explanation)

### Run the interactive demo:

```bash
python3 demo_task_tree.py
```

This provides an interactive demonstration with:
- Visual tree structure
- Tree statistics
- Detailed node results
- Custom task input

## Configuration

### Model Selection

Models are configured in `agent/task_agents.py`:

```python
# Decomposer
self.model = "anthropic.claude-3-haiku-20240307-v1:0"

# Verifier
self.model = "anthropic.claude-3-haiku-20240307-v1:0"

# Solver
self.model = "us.amazon.nova-lite-v1:0"

# Synthesizer
self.model = "us.amazon.nova-lite-v1:0"
```

### Max Depth

To prevent infinite recursion, max tree depth is set in `agent/task_orchestrator.py`:

```python
self.max_depth = 5  # Maximum tree depth
```

## Key Features

### 1. Recursive Decomposition
Tasks are broken down recursively until all branches end in atomic leaf nodes.

### 2. Peer Review Pattern
Each decomposition is verified by a separate agent, ensuring quality.

### 3. Efficient Model Usage
- Fast models (Haiku) for planning and verification
- Small models (Nova Lite) for execution and synthesis
- This optimizes both cost and latency

### 4. Parallel-Ready Structure
Sub-tasks at the same level can potentially be executed in parallel (future enhancement).

### 5. Tree Visualization
The tree structure can be printed for debugging and understanding:

```python
orchestrator.tree.print_tree()
```

## Advantages

1. **Handles Complex Tasks**: Systematically breaks down complex problems
2. **Cost-Efficient**: Uses smaller models for most operations
3. **Transparent**: Tree structure shows how task was decomposed
4. **Quality Control**: Verification phase ensures logical decompositions
5. **Modular**: Each phase is independent and can be improved separately

## Limitations

1. **Sequential Execution**: Currently executes leaves sequentially (could be parallelized)
2. **Depth Limitation**: Max depth prevents infinite recursion but may limit some tasks
3. **Decomposition-Friendly Tasks**: Works best for tasks that can be broken into subtasks
4. **No Dynamic Dependencies**: Assumes sub-tasks are independent (no runtime dependencies)

## Future Enhancements

1. **Parallel Execution**: Execute independent leaf nodes in parallel
2. **Dynamic Depth**: Adjust max depth based on task complexity
3. **Caching**: Cache results for repeated sub-tasks
4. **Progress Tracking**: Real-time progress updates during execution
5. **Alternative Decompositions**: Generate multiple decomposition strategies and choose best
6. **Dependency Resolution**: Handle tasks where sub-tasks depend on each other

## File Structure

```
agent/
├── controller.py           # Main agent controller (updated)
├── task_tree.py           # Tree data structure
├── task_agents.py         # Specialized agents
└── task_orchestrator.py   # Three-phase orchestration

test_task_tree.py          # Test suite
demo_task_tree.py          # Interactive demo
TASK_TREE_IMPLEMENTATION.md # This file
```

## Dependencies

- `strands` and `strands_tools`: Agent framework
- AWS credentials: For Bedrock models (Nova Lite)
- Anthropic models: Via AWS Bedrock (Claude Haiku)

## Troubleshooting

### Issue: Infinite decomposition

**Solution**: Check `max_depth` setting. Tasks that can't be atomized will be marked as leaves at max depth.

### Issue: Poor decomposition quality

**Solution**: The Decomposer and Verifier prompts can be tuned in `agent/task_agents.py`.

### Issue: Slow execution

**Solution**: Consider implementing parallel execution for leaf nodes (future enhancement).

### Issue: Model not found

**Solution**: Ensure AWS credentials are properly configured and models are available in your region.

## Support

For issues or questions:
1. Check logs: The system uses Python logging extensively
2. Enable DEBUG logging in `config/logging.yaml`
3. Run the test suite: `python3 test_task_tree.py`
4. Try the demo: `python3 demo_task_tree.py`

## License

Part of the Iron Man Agent project for Great Agent Hack 2025.
