# Benchmark Evaluation - Quick Start

## Setup Complete ✅

The benchmark evaluation system is fully implemented and ready to run.

## Quick Test (2 minutes)

Test that everything works:

```bash
cd evaluation
python3 test_verifier.py    # Test the LLM verifier API
python3 test_pipeline.py    # Test a couple of prompts
```

## Run Full Benchmark (2-4 hours)

Evaluate all 3 agents across all 3 levels:

```bash
cd evaluation
python3 evaluate_benchmark.py
```

This will:
- Test 3 agents × 3 levels × 25 prompts = **225 total evaluations**
- Save results to `benchmark_results_TIMESTAMP.json`
- Display summary table at the end

## What Gets Tested

### Agents
1. **tree-of-thought-agent** - Claude Sonnet with tree-of-thought
2. **standard-agent** - Dynamic model selection
3. **task-decomposition-tree** - Hierarchical decomposition (your new implementation!)

### Levels
- **L1**: 25 simple prompts (arithmetic, string ops, etc.)
- **L2**: 25 medium prompts (sorting, JSON, etc.)
- **L3**: 25 complex prompts (logic puzzles, algorithms, etc.)

## Metrics Collected

For each agent at each level:
- ✓ Success rate (%)
- ✓ Average time per prompt (seconds)
- ✓ Average cost per prompt (USD)
- ✓ Total cost (USD)
- ✓ List of failed prompts

## Results Location

Results saved to: `benchmark_results_YYYYMMDD_HHMMSS.json`

Example:
```json
{
  "timestamp": "2025-11-16T14:30:00",
  "results": [
    {
      "agent_type": "task-decomposition-tree",
      "level": "L1",
      "success_rate_percent": 85.00,
      "avg_time_per_prompt_seconds": 12.5,
      "avg_cost_per_prompt_usd": 0.0012
    },
    ...
  ]
}
```

## Cost Estimate

Expected total cost for full benchmark:
- Agent costs: ~$0.50 - $2.00
- Verification costs: ~$0.10 - $0.20
- **Total: ~$0.60 - $2.20**

(Varies based on prompt length and model responses)

## Need Help?

See `EVALUATION_README.md` for comprehensive documentation.
