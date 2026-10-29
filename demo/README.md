# Little Tutor demo

From the project root, run `python tutor_demo.py` and open http://127.0.0.1:7860.
No additional Python dependencies are needed. Keep Ollama running with the
`gemma4:e4b` model installed. The page displays a useful error if it cannot connect.

Optional PowerShell settings before starting:

```powershell
$env:TUTOR_MODEL = "gemma4:e4b"
$env:TUTOR_MODEL_URL = "http://localhost:11434/v1/chat/completions"
python tutor_demo.py
```

The demo uses the existing TinyAgent and Memory classes. Each browser tab keeps
its own conversation and sends it to the Python server for each reply. Refresh
or New session clears it. Conversations are limited to 20 completed exchanges
plus one final question. There is no database or tool execution.

## Hosting

Hugging Face Docker Spaces can host the Python server, but the deployed app needs
a model running in that environment or an accessible model service. Its localhost
is not your computer's Ollama. Configure TUTOR_MODEL_URL accordingly. This demo
currently supports an endpoint without API-key authentication; add server-side
authentication support before choosing a provider that requires a key.

For a container, set TUTOR_HOST=0.0.0.0 and PORT=7860 and run tutor_demo.py with
the src and demo directories included. The default loopback binding is for local use.

GitHub Pages can serve demo/index.html, but cannot run tutor_demo.py. The interface
would need a separately hosted backend and a configured API URL to work there.

This project has not been deployed publicly.
