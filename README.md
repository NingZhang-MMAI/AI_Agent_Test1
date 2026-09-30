# AI_Agent_Test1

A local experimental project for understanding how reasoning contributes to AI-agent decision making.

## Working Paper

**From Reasoning to Agency: A Local Experimental Study of Reasoning as a Decision Foundation for AI Agents**

Read the current working paper:

[research/reasoning_agent_study.md](research/reasoning_agent_study.md)

## Current Research Question

> How does the quality and form of reasoning affect the decision-making foundation of an AI agent?

The current empirical scope is intentionally limited to two locally hosted models:

- Gemma 3 12B
- Gemma 4 E4B

The first experiments compare direct prompting, explicit step-by-step prompting, token usage, correctness, and repeated-run consistency.

## Current Results

The completed Gemma 4 E4B experiment found:

- Direct prompt: 321 total tokens, answer = 11
- Step-by-step prompt: 419 total tokens, answer = 11
- Completion-token usage increased by about 33%
- 10/10 repeated runs returned the same final answer

See the paper and the `results/` directory for details.

## Run the Current Experiment

```bash
python reasoning_experiment.py
```

## Research Direction

The project begins with reasoning in isolation and will later extend toward:

```text
Reasoning
  ↓
Planning
  ↓
Tool selection
  ↓
Action
  ↓
Observation
  ↓
Reflection
```

The conceptual bridge to agent behavior is informed by Chain-of-Thought, Self-Consistency, ReAct, and test-time-compute research.
