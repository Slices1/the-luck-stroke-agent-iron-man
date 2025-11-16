# Task Decomposition Tree Agent

## What is This?

A novel AI agent orchestration system that breaks complex tasks into simple sub-tasks using a tree structure, inspired by Abstract Syntax Trees (ASTs) in compilers.

## Quick Start

```bash
# Run via chat interface
python3 chat.py --agent=task-decomposition-tree

# Run interactive demo
python3 demo_task_tree.py

# Run tests
python3 test_task_tree.py
```

## Files in This Implementation

### Core Implementation
- `task_tree.py` - Tree data structure (TaskNode, TaskDecompositionTree)
- `task_agents.py` - Four specialized agents (Decomposer, Verifier, Solver, Synthesizer)
- `task_orchestrator.py` - Three-phase orchestration logic
- `controller.py` - Integration with main agent system (TaskDecompositionTreeAgent class)

### Testing & Demos
- `../test_task_tree.py` - Automated test suite
- `../demo_task_tree.py` - Interactive demonstration

### Documentation
- `../TASK_TREE_IMPLEMENTATION.md` - Full implementation guide
- `../QUICK_START_TASK_TREE.md` - Quick reference
- `../TASK_FLOW_DIAGRAM.md` - Visual flow diagram
- `../IMPLEMENTATION_SUMMARY.md` - Summary of what was built
- This file - README for the agent directory

## How It Works

### Three Phases

**Phase 1: Decomposition (Top-Down)**
- DecomposerAgent breaks complex tasks into 2-5 sub-tasks
- Recursive process continues until all branches end in leaves
- Uses Claude Haiku for fast decomposition

**Phase 2: Verification (Peer Review)**
- VerifierAgent validates each decomposition
- Identifies "leaf nodes" (atomic tasks)
- Also uses Claude Haiku for quality control

**Phase 3: Synthesis (Bottom-Up)**
- SolverAgent executes all leaf nodes
- SynthesizerAgent merges results up the tree
- Uses Amazon Nova Lite for efficient execution

### Example

```
Task: "How do I make breakfast?"
    │
    ├─ Decompose → ["Make toast", "Make tea"]
    │
    ├─ "Make toast"
    │   ├─ Decompose → ["Get bread", "Use toaster"]
    │   ├─ Execute leaves
    │   └─ Synthesize → "Toast ready"
    │
    ├─ "Make tea"
    │   ├─ Decompose → ["Boil water", "Add tea bag"]
    │   ├─ Execute leaves
    │   └─ Synthesize → "Tea ready"
    │
    └─ Final synthesis → "Breakfast ready: toast and tea"
```

## Models Used

| Agent | Model | Purpose |
|-------|-------|---------|
| Decomposer | Claude Haiku | Fast task decomposition |
| Verifier | Claude Haiku | Quality control |
| Solver | Amazon Nova Lite | Execute atomic tasks |
| Synthesizer | Amazon Nova Lite | Merge results |

## API

### TaskDecompositionTreeAgent

Main class in `controller.py`:

```python
from agent.controller import TaskDecompositionTreeAgent

agent = TaskDecompositionTreeAgent()
result = agent.run("Your task here")
```

### TaskOrchestrator

Low-level orchestrator in `task_orchestrator.py`:

```python
from agent.task_orchestrator import TaskOrchestrator

orchestrator = TaskOrchestrator()
result = orchestrator.process_task("Your task here")

# Access the tree
orchestrator.tree.print_tree()

# Get statistics
summary = orchestrator.get_tree_summary()
```

### TaskDecompositionTree

Tree data structure in `task_tree.py`:

```python
from agent.task_tree import TaskDecompositionTree, TaskNode

tree = TaskDecompositionTree("Root task")
node = tree.add_node("Sub-task", parent_id="root")
leaves = tree.get_leaf_nodes()
tree.print_tree()
```

## Configuration

### Max Depth

Configured in `task_orchestrator.py`:

```python
self.max_depth = 5  # Default: 5 levels
```

### Model Selection

Configured in `task_agents.py`:

```python
# Change model IDs here
self.model = "anthropic.claude-3-haiku-20240307-v1:0"
```

## Logging

All components use Python's logging module:

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Or use the project's logging config
from utils.logging_utils import setup_logging
setup_logging()
```

## Error Handling

The system includes comprehensive error handling:

- **Decomposition failures**: Falls back to treating task as leaf
- **Verification failures**: Defaults to safe assumptions
- **Execution failures**: Captures and reports errors
- **Max depth protection**: Prevents infinite recursion

## Performance

### Typical Metrics
- Simple task (2-3 levels): ~10-20 seconds
- Complex task (4-5 levels): ~30-60 seconds
- Model calls per task: 10-20 (depends on tree size)

### Bottlenecks
- Sequential execution of leaf nodes (could be parallelized)
- Sequential synthesis (partially parallelizable)
- Model API latency

## Testing

Run the test suite:

```bash
python3 test_task_tree.py
```

Tests include:
- Simple task decomposition
- Factual question handling
- Complex multi-level tasks
- Error handling

## Future Enhancements

Potential improvements:
- Parallel execution of independent leaves
- Result caching for repeated sub-tasks
- Dynamic depth adjustment
- Progress callbacks
- Dependency resolution between tasks

## Troubleshooting

### Import Errors
```python
# Make sure project root is in path
import sys
sys.path.insert(0, '/path/to/project')
```

### Model Not Found
- Check AWS credentials in `.env`
- Verify model IDs are correct for your region

### Slow Performance
- Normal for complex tasks with many decompositions
- Consider adjusting max_depth to reduce calls
- Future: implement parallel execution

### Poor Decompositions
- Tune prompts in `task_agents.py`
- Adjust verification criteria
- Try different models

## Dependencies

Required packages:
- `strands-agents` - Agent framework
- `strands-agents-tools` - Agent tools
- AWS credentials for Bedrock models

## Architecture Diagram

```
TaskDecompositionTreeAgent (controller.py)
    │
    └── TaskOrchestrator (task_orchestrator.py)
            │
            ├── DecomposerAgent (task_agents.py)
            ├── VerifierAgent (task_agents.py)
            ├── SolverAgent (task_agents.py)
            ├── SynthesizerAgent (task_agents.py)
            │
            └── TaskDecompositionTree (task_tree.py)
                    └── TaskNode (task_tree.py)
```

## Contributing

When modifying this implementation:

1. **Maintain separation of concerns**: Keep tree logic, agents, and orchestration separate
2. **Add tests**: Update `test_task_tree.py` with new test cases
3. **Update documentation**: Keep docs in sync with code changes
4. **Log extensively**: Use logging for debugging
5. **Handle errors gracefully**: Never let exceptions crash the system

## Support

- **Quick Start**: `../QUICK_START_TASK_TREE.md`
- **Full Guide**: `../TASK_TREE_IMPLEMENTATION.md`
- **Flow Diagram**: `../TASK_FLOW_DIAGRAM.md`
- **Implementation Summary**: `../IMPLEMENTATION_SUMMARY.md`

## License

Part of the Iron Man Agent project for Great Agent Hack 2025.

## Status

✅ **Fully Implemented and Tested**

The Task Decomposition Tree Agent is production-ready and integrated with the main agent system.
