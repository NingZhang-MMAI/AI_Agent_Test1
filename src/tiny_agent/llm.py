import json
import urllib.request
from dataclasses import dataclass


@dataclass
class Response:
    """Structured response from LLM calls."""
    content: str = ""
    reasoning: str | None = None
    tool_call: dict | None = None
    metadata: dict | None = None


class LLM:
    def __init__(self, model="gemma4:e4b", url="http://localhost:11434/v1/chat/completions"):
        self.model = model
        self.url = url

    def generate(self, messages) -> Response:
        data = json.dumps({"model": self.model, "messages": messages}).encode("utf-8")
        req = urllib.request.Request(
            url=self.url, data=data, headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as r:
            result = json.loads(r.read())

        message = result["choices"][0]["message"]
        usage = result.get("usage", {})

        return Response(
            content=message.get("content", ""),
            reasoning=message.get("reasoning"),
            metadata={
                "model": result.get("model", self.model),
                "prompt_tokens": usage.get("prompt_tokens"),
                "completion_tokens": usage.get("completion_tokens"),
                "total_tokens": usage.get("total_tokens"),
            },
        )
