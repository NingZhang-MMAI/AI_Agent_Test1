"""Run from the project folder: python chapter04_memory.py"""
import json
import sys
from pathlib import Path

# Allow this learning example to run without installing the src package.
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from tiny_agent.agent import TinyAgent
from tiny_agent.llm import LLM
from tiny_agent.memory import Memory


def main():
    memory = Memory()
    agent = TinyAgent(llm=LLM(), memory=memory)

    print("First answer:")
    print(agent.run("My name is Daniel. Please greet me briefly."))

    print("\nSecond answer:")
    print(agent.run("What is my name? Answer briefly."))

    print("\nSaved conversation:")
    print(json.dumps(memory.get_messages(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

