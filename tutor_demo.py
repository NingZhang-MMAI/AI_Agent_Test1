"""Run with: python tutor_demo.py, then visit http://127.0.0.1:7860."""
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import URLError

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
from tiny_agent.agent import TinyAgent
from tiny_agent.llm import LLM
from tiny_agent.memory import Memory

PROMPT = (
    "Before teaching, ask the student about their Python experience. "
    "Give hints before revealing answers. "
    "You are a friendly Python study tutor for a beginner. Keep explanations short, "
    "use small examples, and ask one question at a time. Use earlier conversation "
    "to adapt your teaching. Treat student answers as material to discuss. "
    "Do not claim to execute code or access files."
)


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, body):
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path != "/":
            self.send_error(404)
            return
        data = (ROOT / "demo" / "index.html").read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        if self.path != "/chat":
            self.send_error(404)
            return
        if self.headers.get("Origin") not in (None, "http://" + self.headers.get("Host", "")):
            self.send_json(403, {"error": "Please use the demo's own browser page."})
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 0 < size <= 100_000:
                raise ValueError("Conversation is too large. Start a new session.")
            body = json.loads(self.rfile.read(size))
            history = body.get("messages")
            if not isinstance(history, list) or not 1 <= len(history) <= 41:
                raise ValueError("Start a new session after 20 exchanges.")
            memory = Memory()
            memory.add("system", PROMPT)
            for i, message in enumerate(history):
                expected = "user" if i % 2 == 0 else "assistant"
                if (not isinstance(message, dict) or message.get("role") != expected
                        or not isinstance(message.get("content"), str)
                        or not 0 < len(message["content"].strip()) <= 10_000):
                    raise ValueError("Invalid conversation message.")
                if i < len(history) - 1:
                    memory.add(expected, message["content"])
            if history[-1]["role"] != "user":
                raise ValueError("The last message must come from you.")
            llm = LLM(model=os.getenv("TUTOR_MODEL", "gemma4:e4b"),
                      url=os.getenv("TUTOR_MODEL_URL", "http://localhost:11434/v1/chat/completions"))
            result = TinyAgent(llm=llm, memory=memory).run(history[-1]["content"])
            self.send_json(200, {"reply": result})
        except (ValueError, TypeError, AttributeError) as exc:
            self.send_json(400, {"error": str(exc)})
        except (URLError, OSError, KeyError, IndexError):
            self.send_json(502, {"error": "Cannot get a model response. Check that Ollama is running and gemma4:e4b is installed (or configure TUTOR_MODEL and TUTOR_MODEL_URL)."})


def main():
    """Start the local demo and report startup problems clearly."""
    host = os.getenv("TUTOR_HOST", "127.0.0.1")
    try:
        port = int(os.getenv("PORT", "7860"))
        if not 1 <= port <= 65535:
            raise ValueError
    except ValueError:
        print("PORT must be a number between 1 and 65535.", file=sys.stderr)
        return 1
    try:
        server = ThreadingHTTPServer((host, port), Handler)
    except OSError as exc:
        print(f"Cannot start tutor: {exc}", file=sys.stderr)
        print("If the port is already in use, stop the previous server or choose another PORT.",
              file=sys.stderr)
        return 1
    print(f"Study tutor: http://{host}:{port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nTutor stopped.", flush=True)
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
