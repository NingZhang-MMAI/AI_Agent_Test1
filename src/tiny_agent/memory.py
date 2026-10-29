"""Chapter 4: conversation history shared across model calls."""


class Memory:
    """Store messages for one agent conversation in memory."""

    def __init__(self):
        self.messages = []

    def add(self, role: str, content: str, tool_call: dict | None = None, **kwargs) -> None:
        message = {"role": role, "content": content}
        if tool_call is not None:
            message["tool_calls"] = [tool_call]
        self.messages.append(message)

    def get_messages(self) -> list[dict]:
        """Return a snapshot of the conversation for the next model call."""
        return [message.copy() for message in self.messages]
