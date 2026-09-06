from tiny_agent.agent import TinyAgent
from tiny_agent.llm import LLM

agent = TinyAgent(llm=LLM())
print(agent.run("What is 2 + 2?"))
print(agent.trajectory.runs)