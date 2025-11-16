# Task Decomposition Tree - Flow Diagram

## Complete Task Flow Example

### Input Task: "How do I make breakfast?"

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER INPUT                                   │
│              "How do I make breakfast?"                          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 1 & 2: TREE BUILDING (Top-Down)                          │
└─────────────────────────────────────────────────────────────────┘

Step 1: Create Root Node
┌─────────────────────────────────────┐
│  [root] "How do I make breakfast?"  │
│  Status: PENDING                    │
└───────────────┬─────────────────────┘
                │
                ▼
Step 2: Verify Root
                │
    ┌───────────┴───────────┐
    │   VerifierAgent       │──── Is this a leaf node?
    │   (Claude Haiku)      │──── Answer: NO (too complex)
    └───────────┬───────────┘
                │
                ▼
Step 3: Decompose Root
                │
    ┌───────────┴───────────┐
    │  DecomposerAgent      │──── Break into sub-tasks
    │  (Claude Haiku)       │
    └───────────┬───────────┘
                │
                ▼
    ["Make toast", "Make tea"]
                │
                ▼
┌───────────────────────────────────────────────┐
│  [root] "How do I make breakfast?"            │
│         Status: DECOMPOSING                   │
│              /            \                   │
│    [node_1]                [node_2]           │
│   "Make toast"            "Make tea"          │
│   Status: PENDING         Status: PENDING     │
└───────────────────────────────────────────────┘

Step 4: Process node_1 ("Make toast")
                │
    ┌───────────┴───────────┐
    │   VerifierAgent       │──── Is "Make toast" a leaf?
    │   (Claude Haiku)      │──── Answer: NO (can decompose)
    └───────────┬───────────┘
                │
                ▼
    ┌───────────┴───────────┐
    │  DecomposerAgent      │──── Break into sub-tasks
    │  (Claude Haiku)       │
    └───────────┬───────────┘
                │
                ▼
    ["Get bread", "Use toaster"]
                │
                ▼
┌────────────────────────────────────────────────┐
│         [node_1] "Make toast"                  │
│         Status: DECOMPOSING                    │
│              /            \                    │
│    [node_3]                [node_4]            │
│   "Get bread"             "Use toaster"        │
│   Status: PENDING         Status: PENDING      │
└────────────────────────────────────────────────┘

Step 5: Process node_3 ("Get bread")
                │
    ┌───────────┴───────────┐
    │   VerifierAgent       │──── Is "Get bread" a leaf?
    │   (Claude Haiku)      │──── Answer: YES (atomic task)
    └───────────┬───────────┘
                │
                ▼
┌────────────────────────────────────────┐
│   [node_3] "Get bread"                 │
│   Status: VERIFIED                     │
│   IS_LEAF: true                        │
└────────────────────────────────────────┘

Step 6: Process node_4 ("Use toaster")
                │
    ┌───────────┴───────────┐
    │   VerifierAgent       │──── Is "Use toaster" a leaf?
    │   (Claude Haiku)      │──── Answer: YES (atomic task)
    └───────────┬───────────┘
                │
                ▼
┌────────────────────────────────────────┐
│   [node_4] "Use toaster"               │
│   Status: VERIFIED                     │
│   IS_LEAF: true                        │
└────────────────────────────────────────┘

Step 7: Process node_2 ("Make tea")
                │
    ┌───────────┴───────────┐
    │   VerifierAgent       │──── Is "Make tea" a leaf?
    │   (Claude Haiku)      │──── Answer: NO (can decompose)
    └───────────┬───────────┘
                │
                ▼
    ┌───────────┴───────────┐
    │  DecomposerAgent      │──── Break into sub-tasks
    │  (Claude Haiku)       │
    └───────────┬───────────┘
                │
                ▼
    ["Boil water", "Add tea bag"]
                │
                ▼
┌────────────────────────────────────────────────┐
│         [node_2] "Make tea"                    │
│         Status: DECOMPOSING                    │
│              /            \                    │
│    [node_5]                [node_6]            │
│   "Boil water"            "Add tea bag"        │
│   Status: PENDING         Status: PENDING      │
└────────────────────────────────────────────────┘

Step 8: Verify remaining nodes
                │
    ┌───────────┴───────────┐
    │   VerifierAgent       │──── All remaining nodes are leaves
    │   (Claude Haiku)      │
    └───────────────────────┘

FINAL TREE STRUCTURE:
┌─────────────────────────────────────────────────────────────────┐
│                [root] "How do I make breakfast?"                 │
│                        Status: VERIFIED                          │
│                    /                      \                      │
│        [node_1] "Make toast"      [node_2] "Make tea"           │
│        Status: VERIFIED           Status: VERIFIED              │
│         /            \              /            \               │
│  [node_3]      [node_4]      [node_5]      [node_6]            │
│ "Get bread"   "Use toaster" "Boil water"  "Add tea bag"        │
│  IS_LEAF       IS_LEAF        IS_LEAF       IS_LEAF             │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  PHASE 3: EXECUTION & SYNTHESIS (Bottom-Up)                      │
└─────────────────────────────────────────────────────────────────┘

Step 9: Execute All Leaf Nodes
                │
    ┌───────────┴───────────────────────────────────┐
    │                                                │
    ▼                  ▼              ▼             ▼
┌─────────┐      ┌─────────┐    ┌─────────┐   ┌─────────┐
│ Solver  │      │ Solver  │    │ Solver  │   │ Solver  │
│ (Nova)  │      │ (Nova)  │    │ (Nova)  │   │ (Nova)  │
└────┬────┘      └────┬────┘    └────┬────┘   └────┬────┘
     │                │              │             │
     ▼                ▼              ▼             ▼
"Get bread     "Place bread    "Boil water   "Add tea bag
from pantry"   in toaster      in kettle"    to cup with
               for 2 mins"                    hot water"

Step 10: Synthesize node_1 ("Make toast")
                │
    ┌───────────┴───────────┐
    │  SynthesizerAgent     │──── Combine sub-results
    │  (Nova Lite)          │
    └───────────┬───────────┘
                │
                ▼
    Sub-results:
    - Get bread: "Get bread from pantry"
    - Use toaster: "Place bread in toaster for 2 mins"
                │
                ▼
    "Toast is ready: Bread was toasted until golden brown"

Step 11: Synthesize node_2 ("Make tea")
                │
    ┌───────────┴───────────┐
    │  SynthesizerAgent     │──── Combine sub-results
    │  (Nova Lite)          │
    └───────────┬───────────┘
                │
                ▼
    Sub-results:
    - Boil water: "Boil water in kettle"
    - Add tea bag: "Add tea bag to cup with hot water"
                │
                ▼
    "Tea is ready: Tea bag steeped in boiling water for 3 minutes"

Step 12: Synthesize root ("How do I make breakfast?")
                │
    ┌───────────┴───────────┐
    │  SynthesizerAgent     │──── Combine sub-results
    │  (Nova Lite)          │
    └───────────┬───────────┘
                │
                ▼
    Sub-results:
    - Make toast: "Toast is ready: Bread was toasted until golden brown"
    - Make tea: "Tea is ready: Tea bag steeped in boiling water"
                │
                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FINAL RESULT                                 │
│                                                                  │
│  "To make breakfast, follow these steps:                        │
│                                                                  │
│   1. Toast: Get bread from the pantry and place it in the      │
│      toaster for about 2 minutes until golden brown.            │
│                                                                  │
│   2. Tea: Boil water in a kettle, then add a tea bag to a cup  │
│      and pour the hot water over it. Let it steep for 3 mins.  │
│                                                                  │
│   Your breakfast of toast and tea is now ready to enjoy!"       │
└─────────────────────────────────────────────────────────────────┘
```

## Model Usage Summary

| Phase | Operation | Model | Count |
|-------|-----------|-------|-------|
| 1 & 2 | Decompose root | Claude Haiku | 1 |
| 1 & 2 | Verify root | Claude Haiku | 1 |
| 1 & 2 | Decompose "Make toast" | Claude Haiku | 1 |
| 1 & 2 | Verify "Get bread" | Claude Haiku | 1 |
| 1 & 2 | Verify "Use toaster" | Claude Haiku | 1 |
| 1 & 2 | Decompose "Make tea" | Claude Haiku | 1 |
| 1 & 2 | Verify "Boil water" | Claude Haiku | 1 |
| 1 & 2 | Verify "Add tea bag" | Claude Haiku | 1 |
| 3 | Execute leaf (4x) | Nova Lite | 4 |
| 3 | Synthesize "Make toast" | Nova Lite | 1 |
| 3 | Synthesize "Make tea" | Nova Lite | 1 |
| 3 | Synthesize root | Nova Lite | 1 |
| **TOTAL** | | **Haiku: 8, Nova: 7** | **15** |

## Key Observations

1. **Efficient Model Usage**:
   - 53% of calls use the cheaper Nova Lite model
   - Haiku only used for planning/verification

2. **Recursive Nature**:
   - Each node is processed independently
   - Depth-first traversal during building
   - Bottom-up synthesis ensures all data flows correctly

3. **Quality Control**:
   - Every decomposition is verified
   - Leaf nodes identified before execution
   - No wasted execution on non-atomic tasks

4. **Parallelization Potential**:
   - Leaf nodes could be executed in parallel
   - Synthesis only waits for direct children
   - Significant speedup possible with concurrency

## Time Flow

```
t=0s    │ User submits task
t=1s    │ Root decomposition starts
t=3s    │ Root decomposed, verification starts
t=4s    │ Root verified as non-leaf, children created
t=5s    │ "Make toast" decomposition starts
t=7s    │ "Make toast" decomposed into 2 leaves
t=8s    │ "Make tea" decomposition starts
t=10s   │ "Make tea" decomposed into 2 leaves
t=11s   │ All 4 leaves verified
t=12s   │ Tree building complete
        │
        │ ---- Phase 3 Begins ----
        │
t=13s   │ Leaf 1: "Get bread" executed
t=15s   │ Leaf 2: "Use toaster" executed
t=17s   │ Leaf 3: "Boil water" executed
t=19s   │ Leaf 4: "Add tea bag" executed
t=20s   │ All leaves completed
t=21s   │ Synthesize "Make toast"
t=23s   │ Synthesize "Make tea"
t=25s   │ Synthesize root
t=26s   │ Final result returned
```

**Total Time: ~26 seconds** (varies with model latency)

## Optimization Opportunities

### Current Implementation
```
Execute leaves:     Sequential (8 seconds)
Synthesize:         Sequential (6 seconds)
Total Phase 3:      14 seconds
```

### With Parallelization (Future)
```
Execute leaves:     Parallel (2 seconds)
Synthesize:         Parallel where possible (3 seconds)
Total Phase 3:      5 seconds
Speedup:           2.8x faster
```

## Error Handling Flow

```
┌─────────────────────────────────────────┐
│  Any Operation Fails                     │
└──────────────┬──────────────────────────┘
               │
               ▼
     ┌─────────────────────┐
     │  Is it a leaf node? │
     └─────────┬───────────┘
          YES  │   NO
               │
    ┌──────────┴──────────┐
    │                     │
    ▼                     ▼
┌─────────┐      ┌──────────────────┐
│ Return  │      │ Mark as leaf and │
│ error   │      │ let solver handle│
│ message │      └─────────┬────────┘
└─────────┘                │
                           ▼
                  ┌────────────────┐
                  │  Solver tries  │
                  │  best effort   │
                  └────────────────┘
```

This ensures the system always produces some result, even if decomposition fails.
