from tiny_agent.agent import TinyAgent
from tiny_agent.llm import LLM
from collections import Counter
 
answers = []
for _ in range(10):
    query = """Six friends (Maarten, Ilse, Sarah, Jor, Irene, and Chris) 
    are sitting in a row.
 
- Sarah is in seat 3.
- Chris is sitting at one of the ends of the row.
- Jor is sitting immediately to the right of Chris.
- Ilse is sitting exactly in the middle of Sarah and Maarten.
- Irene is not sitting next to Sarah.
- Maarten is sitting somewhere to the left of Irene.
 
In which seat is Maarten sitting?
Let's think step by step and give back your answer only after 'Answer:'.
"""
 
    # Generate response
    messages = [{"role": "user", "content": query},]
    response = llm.generate(messages)
    answer = response.content.split("Answer:")[-1].replace("\n", "").strip()
    answers.append(answer)
 
Counter(answers)