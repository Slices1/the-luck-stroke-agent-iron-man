# Benchmark Evaluation System

## Overview

This evaluation system benchmarks all three agents (Tree-of-Thought, Standard, and Task Decomposition Tree) across three difficulty levels (L1, L2, L3).

## Files

### Core Files

1. **`evaluate_benchmark.py`** - Main benchmark orchestrator
   - Runs all agents at all levels
   - Tracks metrics (cost, time, success rate)
   - Saves comprehensive results to JSON
   - Displays summary table

2. **`evaluation_entry_point.py`** - Agent execution wrapper
   - Integrates with actual agent implementations
   - Estimates cost per prompt
   - Returns results in standardized format

3. **`benchmark_prompts.json`** - Test prompts (75 total)
   - 5 tasks per level × 3 levels = 15 tasks
   - 5 prompts per task = 75 prompts total

4. **`benchmark_answers.json`** - Expected answers
   - Corresponding answers for each prompt

### Test Files

5. **`test_verifier.py`** - Tests the LLM verifier API
   - Verifies API connection
   - Tests response format

6. **`test_pipeline.py`** - Tests the evaluation pipeline
   - Quick test with a few prompts
   - Verifies end-to-end integration

## Benchmark Structure

### Difficulty Levels

- **L1 (Simple)**: Basic tasks that require minimal reasoning
  - Arithmetic
  - String reversal
  - Find max number
  - Palindrome check
  - Count vowels

- **L2 (Medium)**: Moderately complex tasks requiring some reasoning
  - Fill-in-the-blank math
  - Sort lists
  - JSON extraction
  - Instruction ordering
  - Find and replace

- **L3 (Complex)**: Complex tasks requiring multi-step reasoning
  - Logic grid puzzles
  - Task dependency planning
  - Data restructuring
  - Simple algorithms
  - Knights & Knaves puzzles

### Agents Under Test

1. **tree-of-thought-agent** - Uses Claude Sonnet 3.5 with tree-of-thought approach
2. **standard-agent** - Uses dynamic model selection based on difficulty
3. **task-decomposition-tree** - Uses hierarchical task decomposition with multiple models

## Usage

### Run the Complete Benchmark

```bash
cd evaluation
python3 evaluate_benchmark.py
```

This will:
- Evaluate all 3 agents at all 3 levels
- Process 75 prompts per agent (225 total)
- Save results to `benchmark_results_TIMESTAMP.json`
- Display summary table

**Expected Duration**: ~2-4 hours for full benchmark (depending on model response times)

### Run a Quick Test

```bash
cd evaluation
python3 test_pipeline.py
```

This runs a quick test with 2 prompts to verify the pipeline works.

### Test the Verifier API

```bash
cd evaluation
python3 test_verifier.py
```

This tests the LLM verifier API connection and response format.

## Metrics Tracked

For each agent at each level:

1. **Success Rate**: Percentage of prompts answered correctly
   - Verified using LLM judge
   - Semantic matching (not exact string match)

2. **Average Time Per Prompt**: Mean time to process each prompt
   - Measured in seconds
   - Includes agent processing time only (not verification)

3. **Average Cost Per Prompt**: Mean cost per prompt
   - Estimated based on model usage
   - Measured in USD
   - Includes agent cost only (verification cost tracked separately)

4. **Total Cost**: Combined cost for all prompts
   - Agent cost + verification cost
   - Measured in USD

## Results Format

Results are saved to `benchmark_results_TIMESTAMP.json`:

```json
{
  "timestamp": "2025-11-16T14:30:00.123456",
  "agents": ["tree-of-thought-agent", "standard-agent", "task-decomposition-tree"],
  "levels": ["L1", "L2", "L3"],
  "results": [
    {
      "agent_type": "task-decomposition-tree",
      "level": "L1",
      "total_prompts": 25,
      "successes": 20,
      "failures": 5,
      "success_rate_percent": 80.00,
      "avg_time_per_prompt_seconds": 12.345,
      "avg_cost_per_prompt_usd": 0.001234,
      "total_agent_cost_usd": 0.030850,
      "total_verification_cost_usd": 0.009525,
      "total_cost_usd": 0.040375,
      "failed_prompts": [...]
    },
    ...
  ]
}
```

## Cost Estimation

### Model Pricing (per 1K tokens)

| Model | Input | Output |
|-------|-------|--------|
| Claude Sonnet 3.5 | $0.003 | $0.015 |
| Claude Haiku | $0.00025 | $0.00125 |
| Amazon Nova Lite | $0.00006 | $0.00024 |

### Cost Estimation Logic

- **task-decomposition-tree**:
  - Assumes ~8 Haiku calls + ~5 Nova Lite calls per prompt
  - Most cost-effective for complex tasks

- **tree-of-thought-agent**:
  - Single Sonnet call per prompt
  - Highest cost but most capable

- **standard-agent**:
  - Dynamic model selection
  - Average cost depends on difficulty distribution

### Verification Cost

- Uses Claude Sonnet 3.5 for verification
- ~$0.0004 per verification (based on actual API response)
- Tracked separately from agent cost

## LLM Verifier

### Configuration

The verifier uses an external API:

```python
LLM_VERIFIER_URL = "https://ctwa92wg1b.execute-api.us-east-1.amazonaws.com/prod/invoke"
```

### Verification Logic

The verifier receives:
- **Expected Answer**: Ground truth from `benchmark_answers.json`
- **Agent Output**: Response from the agent

It returns:
- **"PASSED"**: If agent output is semantically correct
- **"FAILED"**: If agent output is incorrect

Semantic matching allows for variations in phrasing while verifying correctness.

## Customization

### Test Fewer Agents

Edit `evaluate_benchmark.py`:

```python
AGENTS_TO_TEST = [
    'task-decomposition-tree'  # Only test this agent
]
```

### Test Specific Levels

Edit `evaluate_benchmark.py`:

```python
LEVELS = ['L1']  # Only test L1
```

### Adjust Timeout

Edit `evaluate_benchmark.py`:

```python
TIMEOUT_PER_PROMPT = 60  # 1 minute timeout
```

### Modify Cost Estimates

Edit `evaluation_entry_point.py`:

```python
MODEL_PRICING = {
    'anthropic.claude-3-haiku-20240307-v1:0': {'input': 0.00025, 'output': 0.00125},
    # Update with actual pricing
}
```

## Troubleshooting

### "No output from agent"

**Issue**: Agent returned no output

**Solutions**:
- Check that agent initializes correctly
- Verify AWS credentials are set
- Check logs for errors

### "Timeout"

**Issue**: Agent took too long

**Solutions**:
- Increase `TIMEOUT_PER_PROMPT`
- Check if agent is stuck in infinite loop
- Verify model API is responding

### "Agent crashed"

**Issue**: Agent threw an exception

**Solutions**:
- Check error message in results
- Verify all dependencies are installed
- Check that models are accessible

### "Verifier Error"

**Issue**: LLM verifier API failed

**Solutions**:
- Check API credentials
- Verify network connection
- Check API quota/budget

## Expected Results

### Typical Performance

Based on task complexity:

**L1 (Simple Tasks)**:
- Success Rate: 90-100%
- Avg Time: 5-15 seconds
- Avg Cost: $0.0005-$0.002

**L2 (Medium Tasks)**:
- Success Rate: 70-90%
- Avg Time: 10-25 seconds
- Avg Cost: $0.001-$0.004

**L3 (Complex Tasks)**:
- Success Rate: 50-80%
- Avg Time: 20-60 seconds
- Avg Cost: $0.002-$0.008

### Agent Comparison

Expected rankings:

1. **tree-of-thought-agent**: Highest success rate, highest cost
2. **task-decomposition-tree**: Good success rate, moderate cost
3. **standard-agent**: Variable performance, lowest cost

## Adding New Benchmarks

### 1. Add Prompts

Edit `benchmark_prompts.json`:

```json
{
  "L1: Task 6 (New Task)": [
    "Prompt 1",
    "Prompt 2",
    ...
  ]
}
```

### 2. Add Answers

Edit `benchmark_answers.json`:

```json
{
  "L1: Task 6 (New Task)": [
    "Answer 1",
    "Answer 2",
    ...
  ]
}
```

### 3. Run Benchmark

The new tasks will be automatically included in the next run.

## Performance Optimization

### Parallel Execution (Future Enhancement)

Currently, prompts are evaluated sequentially. For faster evaluation:

1. Implement parallel subprocess execution
2. Use process pool for agent calls
3. Rate-limit API calls to avoid quota issues

### Caching (Future Enhancement)

For repeated evaluations:

1. Cache agent responses by prompt hash
2. Skip re-evaluation of unchanged prompts
3. Only verify new/changed responses

## Support

For issues or questions:

1. Check this README
2. Run test scripts (`test_verifier.py`, `test_pipeline.py`)
3. Review error messages in results JSON
4. Check agent logs in project root

## Status

✅ **Fully Implemented**

- Verifier API: Tested and working
- Evaluation pipeline: Complete
- Multi-agent support: Implemented
- Multi-level support: Implemented
- Metrics tracking: Complete
- Results saving: Implemented
- Documentation: Complete

Ready for full benchmark evaluation!
