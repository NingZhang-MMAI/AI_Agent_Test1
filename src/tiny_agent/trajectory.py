class Trajectory:
    """Records what the agent did."""

    def __init__(self):
        self.runs = []

    def initialize(self, task: str):
        self.runs.append({"task": task, "steps": []})

    def add(self, response):
        self.runs[-1]["steps"].append(response)