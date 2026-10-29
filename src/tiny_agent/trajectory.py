from dataclasses import dataclass


@dataclass
class Step:
    """A single step in an agent's trajectory."""

    thought: str = ""
    action: dict | None = None
    observation: str | None = None
    answer: str | None = None
    metadata: dict | None = None


class Trajectory:
    """Records agent execution as a sequence of runs.

    Each run is a dict with keys "query" (str) and "steps" (list[Step]).
    """

    def __init__(self):
        self.runs = []

    def initialize(self, task: str):
        self.runs.append({"query": task, "steps": []})

    def add(self, response, observation: str | None = None):
        step = Step(
            thought=response.reasoning or "",
            metadata=response.metadata,
        )
        if observation is not None:
            step.action = response.tool_call
            step.observation = observation
        else:
            step.answer = response.content
        self.runs[-1]["steps"].append(step)
