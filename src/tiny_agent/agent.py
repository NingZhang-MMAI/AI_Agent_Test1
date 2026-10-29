
from .llm import LLM
from .memory import Memory
from .trajectory import Trajectory



class TinyAgent:
    """A minimal, modular, and educational agent framework."""

    def __init__(self, llm: LLM, memory: Memory | None = None):
        self.llm = llm
        self.memory = memory if memory is not None else Memory()
        self.tools = None  # Chapter 5: Add Tools
        self.planner = None  # Chapter 6: Add Planning

        self.trajectory = Trajectory()

    def run(self, task: str) -> str:
        """Run the agent on a task."""
        self.memory.add("user", task)
        self.trajectory.initialize(task)
        return self._step()

    def _step(self) -> str:
        """Perform a single step."""
        messages = self.memory.get_messages()
        response = self.llm.generate(messages)
        self.memory.add("assistant", response.content)
        self.trajectory.add(response)
        return response.content

    def _execute_action(self, action: str) -> str | None:
        """Execute a tool action."""
        # Placeholder - will be implemented in later chapters
        return f"Executed action: {action}"
