# From Reasoning to Agency: A Local Experimental Study of Reasoning as a Decision Foundation for AI Agents

**Working Paper — Version 0.1**  
**Repository:** AI_Agent_Test1  
**Status:** Initial Gemma 4 experiment completed; Gemma 3 comparison planned

## Abstract

Reasoning is often discussed as a capability that improves language-model answers, but in an AI agent it has a broader role: reasoning helps connect a goal to a sequence of decisions and actions. Prior work on Chain-of-Thought (CoT) prompting showed that intermediate reasoning steps can improve complex problem solving, while ReAct demonstrated how reasoning can be interleaved with actions and observations in an agent loop. This study isolates the reasoning component before introducing a full action environment.

Using a minimal Python agent framework (TinyAgent), Ollama, and locally hosted Gemma models, I study how different forms of reasoning affect correctness, consistency, and inference cost. The first completed experiment uses Gemma 4 E4B and compares a direct prompt with an explicit step-by-step prompt. Both conditions produced the correct answer on a simple state-tracking problem, but explicit step-by-step prompting increased completion tokens from 272 to 362 (about 33%) and total tokens from 321 to 419 (about 31%). Ten repeated runs produced the same final answer, showing high consistency under the tested configuration but no meaningful diversity for self-consistency voting.

The next stage will compare Gemma 3 12B and Gemma 4 E4B under the same direct and step-by-step prompts. The broader research question is how the form and quality of reasoning affect the decision-making foundation required for later agent capabilities such as planning, tool selection, and reflection.

---

## 1. Introduction

Large language models can generate useful answers directly from text prompts. An AI agent, however, must do more than produce a response. It may need to decide what information is missing, choose an action, use a tool, interpret the result, revise its plan, and determine whether the goal has been completed.

This makes reasoning important not only as a way to improve answers, but as a possible **decision layer** within an agent.

This framing is closely related to the ReAct approach, which interleaves reasoning traces with actions and observations. Rather than immediately implementing a complete ReAct-style agent, this study begins by isolating the reasoning component in a small local setup.

The objective is not to claim that two local models represent all reasoning systems. Instead, the project is a limited empirical study designed to answer a narrower question first:

> **How do prompt-induced reasoning and native reasoning differ in two locally hosted Gemma models, and what do those differences imply for the reasoning foundation of an AI agent?**

The project is intentionally incremental. The first phase studies reasoning in isolation. Later work can extend the same experimental framework to tool selection, planning, reflection, and full agent trajectories.

---

## 2. Research Question and Scope

### 2.1 Main research question

> **How does the quality and form of reasoning affect the decision-making foundation of an AI agent?**

This question is broader than the experiments in the first version of the paper. Therefore, the empirical scope is deliberately restricted.

### 2.2 Phase 1 empirical question

> **How do prompt-induced reasoning and native reasoning differ between Gemma 3 12B and Gemma 4 E4B in terms of correctness, consistency, and inference cost?**

### 2.3 Current scope

This version focuses on:

- two locally hosted models:
  - Gemma 3 12B
  - Gemma 4 E4B
- direct prompting
- explicit step-by-step prompting
- correctness
- prompt, completion, and total token usage
- repeated-run consistency

This version does **not** yet test:

- tool use
- action selection
- planning
- reflection
- memory
- full ReAct loops
- end-to-end agent task completion

Those capabilities are reserved for later phases.

---

## 3. Related Work

### 3.1 Chain-of-Thought prompting

Wei et al. introduced **Chain-of-Thought Prompting**, showing that providing intermediate reasoning demonstrations can improve performance on arithmetic, commonsense, and symbolic reasoning tasks. The central idea is that instead of mapping directly from question to answer, the model generates intermediate reasoning steps.

This motivates the first comparison in this study: direct prompting versus an explicit step-by-step reasoning instruction.

### 3.2 Self-consistency

Wang et al. proposed **self-consistency**, which samples multiple reasoning paths and chooses the most consistent final answer rather than relying on a single greedy reasoning trajectory.

This motivates the repeated-run experiment in this project.

### 3.3 ReAct: reasoning linked to acting

Yao et al. proposed **ReAct**, which combines reasoning traces with actions and observations. ReAct is particularly important to this project because it provides the conceptual bridge between reasoning and agency.

The present study does not yet reproduce a complete ReAct agent. Instead, it isolates the reasoning layer that would later support action selection, planning, and revision.

### 3.4 Test-time compute

Snell et al. studied how additional test-time computation can improve language-model performance and showed that the effectiveness of extra inference compute depends on task difficulty and how that compute is allocated.

This is relevant because longer reasoning is not automatically better. A simple task may already be solved correctly without additional reasoning, in which case extra reasoning may primarily increase inference cost.

---

## 4. Conceptual Framework

This study distinguishes **form of reasoning** from **quality of reasoning**.

### 4.1 Form of reasoning

The form describes how reasoning behavior is produced.

#### Direct generation

The model answers the question without an explicit instruction to produce intermediate reasoning.

#### Prompt-induced reasoning

The model is explicitly instructed to reason step by step before producing an answer.

#### Native reasoning

The model has been trained or post-trained to produce reasoning behavior without requiring an explicit step-by-step instruction.

#### Search-enhanced reasoning

Multiple candidate reasoning paths are generated and then compared using consistency or a verifier before selecting a final answer.

### 4.2 Quality of reasoning

Reasoning quality is not measured by response length alone. For later agent experiments, useful dimensions include:

- correctness
- logical decomposition
- next-action accuracy
- consistency
- ability to recover from errors
- efficiency

In Phase 1, the measurable dimensions are restricted to:

- final-answer correctness
- token usage
- repeated-run consistency

### 4.3 Link to agent decision-making

In the longer-term project, reasoning will be studied as a foundation for task decomposition, planning, action or tool selection, interpretation of observations, reflection, and revision of decisions. The present experiments study only the reasoning component.

---

## 5. Experimental Environment

### 5.1 Software architecture

The experimental system uses a minimal TinyAgent written in Python. TinyAgent sends requests through an LLM wrapper to a locally hosted Ollama endpoint, receives the model response, and records the output and experiment metadata.

### 5.2 Local inference

The models are served locally through Ollama using an OpenAI-compatible chat-completions endpoint.

Current model used in the completed experiment:

- **Gemma 4 E4B**
- approximately 4B effective parameters
- native reasoning behavior available through the model/API

Planned comparison model:

- **Gemma 3 12B**
- 12B parameters
- used as the non-native-reasoning comparison model in the planned experiment

### 5.3 Recorded metrics

For each run, the experiment records:

- model
- prompt condition
- model response
- parsed final answer where applicable
- prompt tokens
- completion tokens
- total tokens

Results are stored in:

- `results/reasoning_experiment.json`
- `results/reasoning_experiment.csv`
- `results/self_consistency.svg`

The experiment script is:

- `reasoning_experiment.py`

---

## 6. Experiment 1: Direct Prompt on Gemma 4 E4B

### 6.1 Task

The initial task was intentionally simple:

> I saw 9 penguins. 2 slid into the water and disappeared from sight while 4 waddled up from the shore. How many can I see?

The expected answer is:

```text
11
```

### 6.2 Prompt condition

No explicit "think step by step" instruction was added.

### 6.3 Observed output

The model returned the correct answer and provided a short decomposition:

```text
You can see 11 penguins.

1. Start: 9 penguins
2. Disappear: 9 - 2 = 7
3. Appear: 7 + 4 = 11
```

### 6.4 Token usage

| Metric | Value |
|---|---:|
| Prompt tokens | 49 |
| Completion tokens | 272 |
| Total tokens | 321 |
| Final answer | 11 |

### 6.5 Methodological observation

The API response also contained a reasoning field.

This is important because my initial implementation did not explicitly disable Gemma 4's native reasoning behavior. Therefore, this condition should **not** be interpreted as a true non-reasoning baseline.

The more accurate interpretation is:

> **Gemma 4 native reasoning under a direct user prompt.**

This distinction changes how Experiment 2 should be interpreted.

---

## 7. Experiment 2: Explicit Step-by-Step Prompt on Gemma 4 E4B

### 7.1 Prompt modification

The same question was used, but the following instruction was added:

```text
Let's think step by step.
```

The model and task remained unchanged.

### 7.2 Observed result

The model again returned the correct answer, 11, with a more explicitly structured response.

### 7.3 Token usage

| Metric | Direct | Step-by-step |
|---|---:|---:|
| Prompt tokens | 49 | 57 |
| Completion tokens | 272 | 362 |
| Total tokens | 321 | 419 |
| Final answer | 11 | 11 |

### 7.4 Token increase

Completion-token increase:

```text
(362 - 272) / 272 ≈ 33.1%
```

Total-token increase:

```text
(419 - 321) / 321 ≈ 30.5%
```

### 7.5 Finding

The explicit step-by-step instruction substantially increased generated tokens but did not improve final-answer accuracy on this simple task.

This supports a limited conclusion:

> **For a simple problem already solved correctly by Gemma 4 E4B, additional explicit reasoning increased inference output without producing a measurable accuracy improvement.**

It does **not** support the stronger conclusion that explicit reasoning is generally unnecessary. Harder tasks may produce different results.

---

## 8. Experiment 3: Repeated Reasoning and Consistency

### 8.1 Procedure

The reasoning task was repeated ten times. Each response was instructed to end with:

```text
FINAL_ANSWER: <number>
```

The script parsed the final answer from each run.

### 8.2 Results

```text
Answer 11: 10 / 10 runs
Other answers: 0 / 10 runs
```

Observed answer consistency:

```text
10 / 10 = 100%
```

Each repeated run recorded:

| Metric | Value per run |
|---|---:|
| Prompt tokens | 69 |
| Completion tokens | 407 |
| Total tokens | 476 |
| Parsed answer | 11 |

### 8.3 Interpretation

The experiment demonstrated **consistency**, but it did not yet demonstrate meaningful self-consistency search.

The ten responses were effectively identical. Self-consistency becomes more informative when sampling produces different reasoning paths or different candidate answers.

Therefore:

> **The current configuration produced insufficient reasoning diversity to evaluate majority-vote self-consistency meaningfully.**

This is a useful negative result because it identifies a requirement for future experimental design: harder tasks and/or increased sampling diversity.

---

## 9. Current Results Summary

| Experiment | Model | Prompt condition | Total tokens | Final result |
|---|---|---|---:|---|
| Direct prompt | Gemma 4 E4B | Normal | 321 | 11 |
| Explicit CoT | Gemma 4 E4B | "Let's think step by step" | 419 | 11 |
| Repeated reasoning | Gemma 4 E4B | reasoning prompt, 10 runs | 476/run | 11 in 10/10 |

### Current findings

1. Gemma 4 E4B exhibited reasoning behavior without an explicit CoT instruction.
2. Explicit step-by-step prompting increased completion tokens by approximately 33%.
3. Explicit step-by-step prompting did not change correctness on the simple test problem.
4. Ten repeated runs produced the same answer.
5. The repeated-run condition lacked enough diversity to test self-consistency voting meaningfully.
6. The original direct condition was not a true non-reasoning baseline because native reasoning was still available.

---

## 10. Planned Two-Model Comparison

The next experiment is intentionally limited to the same two local models.

### 10.1 Experimental matrix

| Condition | Model | Prompt form | Status |
|---|---|---|---|
| A | Gemma 3 12B | Direct | Planned |
| B | Gemma 3 12B | Step-by-step | Planned |
| C | Gemma 4 E4B | Direct | Initial result available |
| D | Gemma 4 E4B | Step-by-step | Initial result available |

### 10.2 Main comparison

The experiment is designed to distinguish four conditions: a Gemma 3 12B direct-prompt baseline, Gemma 3 12B with prompt-induced Chain-of-Thought reasoning, Gemma 4 E4B with native reasoning under a direct prompt, and Gemma 4 E4B with both native reasoning and an explicit step-by-step instruction.

### 10.3 Planned measures

For both models and both prompt conditions:

- answer correctness
- average prompt tokens
- average completion tokens
- average total tokens
- repeated-run consistency
- answer distribution

No Gemma 3 numerical results are reported in this version because that experiment has not yet been run.

---

## 11. Hypotheses for the Two-Model Study

### H1

**Explicit step-by-step prompting will have a larger effect on Gemma 3 12B than on Gemma 4 E4B.**

Rationale: Gemma 3 provides the prompt-induced reasoning condition, while Gemma 4 already has native reasoning capability.

### H2

**Gemma 4 E4B will display reasoning behavior without requiring an explicit CoT instruction.**

The first completed experiment is consistent with this hypothesis, but additional tasks are needed before drawing a broader conclusion.

### H3

**Additional reasoning will increase inference token usage, while its accuracy benefit will depend on task difficulty.**

The first simple task supports the token-cost part of this hypothesis but is too easy to evaluate the accuracy-benefit component.

---

## 12. Discussion

### 12.1 Reasoning length is not reasoning quality

One of the clearest lessons from the initial experiment is that longer reasoning should not automatically be treated as better reasoning.

The step-by-step condition generated substantially more tokens, but both conditions reached the same correct answer.

For the simple task tested here, additional explicit reasoning produced more tokens while reaching the same correct answer. Harder tasks may show a different relationship if additional reasoning improves decomposition or error detection.

The experiment therefore motivates measuring both **quality** and **cost**, not reasoning length alone.

### 12.2 Prompt-induced reasoning and native reasoning should be separated

A central methodological lesson is that the source of reasoning matters.

A non-native model prompted with Chain-of-Thought and a native reasoning model given a normal prompt are not equivalent experimental conditions.

Both may produce visible step-by-step behavior, but they arise from different model and inference configurations.

The planned Gemma 3 / Gemma 4 comparison is intended to examine this difference more directly.

### 12.3 Why this matters for agents

The significance of the study is not the penguin arithmetic problem itself.

The longer-term question is whether different reasoning approaches lead to different **decisions** when the model becomes part of an agent.

A later agent may need to decide what information is missing, which tool to use, whether a tool result solved the problem, whether to revise the plan, whether another action is needed, and when the task is complete.

ReAct provides a useful conceptual model for this transition because it interleaves reasoning with actions and environmental observations.

Phase 1 therefore isolates the reasoning layer before introducing these additional sources of complexity.

---

## 13. Limitations

The current study has several important limitations:

1. Only Gemma 4 E4B has completed experimental results in this version.
2. The initial task is intentionally simple and cannot establish performance on difficult reasoning tasks.
3. The initial direct condition did not disable native reasoning.
4. Only ten repeated runs were used.
5. The repeated runs did not produce diverse reasoning trajectories.
6. Token counts measure inference activity, not reasoning quality directly.
7. No agent actions, tools, memory, planning, or reflection are tested yet.
8. Results from two local models should not be generalized to language models broadly.

These limitations define the next experiments rather than invalidate the initial observations.

---

## 14. Future Work

The immediate next step is intentionally narrow:

### Phase 1 extension

- run Gemma 3 12B under the same experimental harness
- compare direct and step-by-step prompts
- repeat both Gemma 3 and Gemma 4 experiments over a small set of objectively scorable reasoning tasks
- introduce controlled sampling diversity
- compare accuracy, consistency, and inference cost

Only after the two-model study is complete will the project expand toward agent behavior.

### Later phases

Later phases will extend the study from reasoning comparison to task decomposition, planning, tool selection, ReAct-style interaction, reflection and error recovery, and eventually end-to-end TinyAgent evaluation.

The later phases will more directly test the broader research question of how reasoning affects agent decision-making.

---

## 15. Conclusion

This working paper begins with a simple premise: reasoning in an AI agent should be studied not only as a way to produce an answer, but as a potential foundation for making decisions.

The first local Gemma 4 E4B experiment found that explicit step-by-step prompting increased completion-token usage by approximately 33% while producing the same correct answer as the direct condition. Ten repeated runs returned the same answer, showing high consistency but insufficient diversity for meaningful self-consistency voting.

These observations are preliminary. The next experiment will compare Gemma 3 12B and Gemma 4 E4B under controlled direct and step-by-step prompting. The purpose is to distinguish prompt-induced reasoning from native reasoning before introducing the additional complexity of tools, planning, actions, and environmental feedback.

The broader direction is inspired by the transition from Chain-of-Thought reasoning to ReAct-style agency, where reasoning informs decisions, actions produce observations, and those observations can inform subsequent reasoning. Understanding the reasoning layer first provides a clearer foundation for studying the complete agent later.

---

## References

1. Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E. H., Le, Q. V., & Zhou, D. (2022). **Chain-of-Thought Prompting Elicits Reasoning in Large Language Models.** *Advances in Neural Information Processing Systems (NeurIPS 2022)*. https://proceedings.neurips.cc/paper_files/paper/2022/hash/9d5609613524ecf4f15af0f7b31abca4-Abstract.html

2. Wang, X., Wei, J., Schuurmans, D., Le, Q. V., Chi, E. H., Narang, S., Chowdhery, A., & Zhou, D. (2023). **Self-Consistency Improves Chain of Thought Reasoning in Language Models.** *International Conference on Learning Representations (ICLR 2023)*. https://openreview.net/forum?id=1PL1NIMMrw

3. Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K. R., & Cao, Y. (2023). **ReAct: Synergizing Reasoning and Acting in Language Models.** *International Conference on Learning Representations (ICLR 2023)*. https://openreview.net/forum?id=WE_vluYUL-X

4. Snell, C., Lee, J., Xu, K., & Kumar, A. (2024). **Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters.** arXiv:2408.03314. https://arxiv.org/abs/2408.03314

---

## Reproducibility

Current experiment:

```bash
python reasoning_experiment.py
```

Generated results:

```text
results/
├── reasoning_experiment.json
├── reasoning_experiment.csv
└── self_consistency.svg
```

The repository will be updated as the Gemma 3 comparison and later experiments are completed.
