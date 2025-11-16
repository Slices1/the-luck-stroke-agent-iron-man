# Task Decomposition Tree - Quick Start Guide

## What is it?

A novel multi-agent system that breaks complex tasks into simple sub-tasks, executes them, and merges results back together - like a tree!

## How it Works (30-second version)

```
1. DECOMPOSE: "Make breakfast" → ["Make toast", "Make tea"]
                                      ↓              ↓
2. VERIFY:     Check if atomic?    DECOMPOSE     DECOMPOSE
                                      ↓              ↓
                                 ["Get bread",  ["Boil water",
                                  "Use toaster"] "Add tea bag"]
                                      ↓              ↓
3. EXECUTE:    (All leaf nodes executed by small AI)
                                      ↓              ↓
4. SYNTHESIZE: Merge results back up the tree
                                      ↓
                         "Breakfast is ready!"
```

## Quick Usage

### Method 1: Via Chat Interface

```bash
python3 chat.py --agent=task-decomposition-tree
```

Then type your task when prompted.

### Method 2: Interactive Demo

```bash
python3 demo_task_tree.py
```

Follow the prompts to see the tree structure and results.

### Method 3: Run Tests

```bash
python3 test_task_tree.py
```

## Models Used

- **Decomposer**: Claude Haiku (fast decomposition)
- **Verifier**: Claude Haiku (quality control)
- **Solver**: Amazon Nova Lite (executes leaves)
- **Synthesizer**: Amazon Nova Lite (merges results)

## Key Features

✓ Handles complex multi-step tasks
✓ Uses smaller/cheaper models for most work
✓ Shows tree structure for transparency
✓ Quality control via verification phase
✓ Prevents infinite loops with max depth

## Example Tasks

**Simple**: "How do I make a cup of tea?"
**Medium**: "Explain the water cycle"
**Complex**: "How does photosynthesis work?"

## When to Use This Agent?

**Good for**:
- Tasks that can be broken into steps
- Educational explanations
- Multi-part questions
- "How to" questions

**Not ideal for**:
- Single simple questions ("What is 2+2?")
- Tasks where steps depend on each other's results
- Real-time data queries

## File Structure

```
agent/
├── task_tree.py          # Tree data structure
├── task_agents.py        # The 4 specialized agents
├── task_orchestrator.py  # 3-phase orchestration
└── controller.py         # Integration with main system

demo_task_tree.py         # Interactive demo
test_task_tree.py         # Test suite
```

## Troubleshooting

**Agent not found?**
- Make sure you're using: `--agent=task-decomposition-tree`

**Import errors?**
- Check that strands is installed: `pip3 install strands-agents`

**AWS errors?**
- Verify your .env file has AWS credentials

**Slow execution?**
- Normal! The tree building process makes multiple LLM calls

## Need Help?

1. Read the full documentation: `TASK_TREE_IMPLEMENTATION.md`
2. Check the logs (set DEBUG in `config/logging.yaml`)
3. Try the demo: `python3 demo_task_tree.py`

## Three Phases Explained

### Phase 1: Decomposition
Break tasks into smaller sub-tasks recursively

### Phase 2: Verification
Check if decomposition is good and if tasks are atomic

### Phase 3: Synthesis
Execute leaves and merge results up the tree

## That's it!

You now know how to use the Task Decomposition Tree Agent. Try it with your own tasks!
