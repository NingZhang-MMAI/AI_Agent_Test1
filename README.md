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

The project begins with reasoning in isolation and will later extend toward planning, tool selection, action, observation, and reflection. The conceptual bridge to agent behavior is informed by Chain-of-Thought, Self-Consistency, ReAct, and test-time-compute research.

---

# Tiny Agent â€” Python Study Tutor

A learning project for building a small AI agent with conversation memory.
The Little Tutor web demo uses the project's `TinyAgent`, `Memory`, and `LLM`
classes to teach Python through short explanations and questions.

## Run locally on Windows

You need Python 3.10 or newer and Ollama with the `gemma4:e4b` model installed.
The tutor demo uses Python's standard library; no additional packages are needed.

1. Open PowerShell in the project folder.
2. If Ollama is not already running, start it:

   ```powershell
   ollama serve
   ```

3. In another terminal, check your models and download the model if needed:

   ```powershell
   ollama list
   ollama pull gemma4:e4b
   ```

   Skip the download if the model is already listed.

4. Start the demo from the repository root:

   ```powershell
   python tutor_demo.py
   ```

5. Open Chrome, Edge, or Firefox and enter:

   ```text
   http://localhost:7860
   ```

   You can also open the page from PowerShell:

   ```powershell
   Start-Process "http://localhost:7860"
   ```

Keep the Python server running while using the page. Press Ctrl+C in its terminal
to stop it. The first model response can take a while as Ollama loads the model.

## Test conversation memory

1. Send: `My name is Daniel. I am learning Python.`
2. Ask: `What is my name?`
3. Click **New session** and ask the same question again.

The tutor should recall the name during the first conversation. After resetting,
the previous conversation is no longer supplied to the model. Refreshing the page
also clears the conversation. Replies are model-generated and may be incorrect.

## Troubleshooting

### PowerShell says â€œollama is not recognizedâ€

The terminal cannot find the Ollama executable. Ollama may still be running as a
desktop application. Check its local API:

```powershell
Invoke-RestMethod http://localhost:11434/api/tags
```

If this returns your models, skip `ollama serve` and start the Python demo.
Otherwise, install or launch Ollama, then open a new terminal so it picks up any
updated PATH setting.

### â€œAddress already in useâ€

If this happens with `ollama serve`, Ollama may already be running. Use the API
check above. If it happens with `python tutor_demo.py`, try opening the webpage;
an earlier demo server may already be running. Alternatively choose another port:

```powershell
$env:PORT = "7861"
python tutor_demo.py
```

Then visit http://localhost:7861.

### The page opens but the tutor cannot respond

Check that Ollama is running and `gemma4:e4b` is installed. To select a different
installed model or a compatible endpoint, set these before starting the demo:

```powershell
$env:TUTOR_MODEL = "gemma4:e4b"
$env:TUTOR_MODEL_URL = "http://localhost:11434/v1/chat/completions"
python tutor_demo.py
```

## Follow one message through the code

1. `demo/index.html` sends the conversation to `/chat`.
2. `tutor_demo.py` creates the tutor instructions and restores earlier messages.
3. `TinyAgent.run()` adds the new question to `Memory`.
4. `TinyAgent._step()` gets the conversation and calls `LLM.generate()`.
5. `LLM.generate()` sends the messages to Ollama and reads its response.
6. The agent stores the answer and records the result in its trajectory.
7. The server returns the answer for the webpage to display.

Each browser tab keeps its own conversation in memory. The server reconstructs
the agent's conversation on each request. There is no database, file access, or
code execution tool in the tutor demo.

## Hosting

Uploading this repository to GitHub saves and shares the source code; it does
not automatically start the tutor website.

- **GitHub Pages** can host static HTML/CSS/JavaScript, but the Python backend
  needs separate hosting.
- **Hugging Face Docker Spaces** can run the Python server. A Space also needs a
  model running there or an accessible model API: its `localhost` cannot reach
  Ollama on your computer. See [demo/README.md](demo/README.md) for configuration.

References: [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
and [Hugging Face Docker Spaces](https://huggingface.co/docs/hub/spaces-sdks-docker).

