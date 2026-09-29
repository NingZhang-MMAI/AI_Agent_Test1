"""Run small, reproducible reasoning experiments against the local TinyAgent.

The script writes raw outputs and a simple SVG chart to ./results so the
Substack article can cite real runs from this repository.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from tiny_agent.agent import TinyAgent
from tiny_agent.llm import LLM


RESULTS_DIR = ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)

PUZZLE = (
    "I saw 9 penguins. 2 slid into the water and disappeared from sight "
    "while 4 waddled up from the shore. How many can I see?"
)

SELF_CONSISTENCY_PROMPT = (
    PUZZLE
    + "\nThink through the problem carefully. "
      "End your response with exactly: FINAL_ANSWER: <number>"
)


def run_once(agent: TinyAgent, label: str, prompt: str) -> dict:
    answer = agent.run(prompt)
    response = agent.trajectory.runs[-1]["steps"][-1]
    return {
        "label": label,
        "prompt": prompt,
        "content": answer,
        "reasoning": response.reasoning,
        "metadata": response.metadata or {},
    }


def extract_final_number(text: str) -> str:
    match = re.search(r"FINAL_ANSWER:\s*(-?\d+(?:\.\d+)?)", text, re.IGNORECASE)
    if match:
        return match.group(1)

    numbers = re.findall(r"-?\d+(?:\.\d+)?", text)
    return numbers[-1] if numbers else "unparsed"


def write_svg_bar_chart(counts: Counter[str], path: Path) -> None:
    items = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    width = 760
    left = 170
    top = 70
    bar_h = 34
    gap = 18
    chart_w = 500
    max_count = max(counts.values()) if counts else 1
    height = max(220, top + len(items) * (bar_h + gap) + 60)

    rows = []
    for i, (answer, count) in enumerate(items):
        y = top + i * (bar_h + gap)
        bar_w = int(chart_w * count / max_count)
        rows.append(
            f'<text x="20" y="{y + 23}" font-size="18">Answer {answer}</text>'
            f'<rect x="{left}" y="{y}" width="{bar_w}" height="{bar_h}" rx="4" '
            f'fill="#4f46e5" />'
            f'<text x="{left + bar_w + 12}" y="{y + 23}" font-size="18">{count}</text>'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" fill="white"/>
<text x="20" y="36" font-size="24" font-weight="700">Self-consistency: answer frequency</text>
<text x="20" y="58" font-size="14">Local Gemma model via TinyAgent</text>
{"".join(rows)}
</svg>'''
    path.write_text(svg, encoding="utf-8")


def main() -> None:
    llm = LLM()
    agent = TinyAgent(llm=llm)

    timestamp = datetime.now(timezone.utc).isoformat()

    direct = run_once(agent, "direct", PUZZLE)
    cot = run_once(
        agent,
        "zero_shot_cot",
        PUZZLE + " Let's think step by step.",
    )

    self_consistency_runs = []
    for i in range(10):
        run = run_once(agent, f"self_consistency_{i + 1}", SELF_CONSISTENCY_PROMPT)
        run["parsed_answer"] = extract_final_number(run["content"])
        self_consistency_runs.append(run)

    counts = Counter(run["parsed_answer"] for run in self_consistency_runs)

    result = {
        "timestamp_utc": timestamp,
        "model": llm.model,
        "puzzle": PUZZLE,
        "direct": direct,
        "zero_shot_cot": cot,
        "self_consistency": {
            "runs": self_consistency_runs,
            "answer_counts": dict(counts),
        },
    }

    (RESULTS_DIR / "reasoning_experiment.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    with (RESULTS_DIR / "reasoning_experiment.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "label",
                "parsed_answer",
                "prompt_tokens",
                "completion_tokens",
                "total_tokens",
                "content",
            ],
        )
        writer.writeheader()

        for run in [direct, cot] + self_consistency_runs:
            metadata = run.get("metadata") or {}
            writer.writerow(
                {
                    "label": run["label"],
                    "parsed_answer": run.get("parsed_answer", ""),
                    "prompt_tokens": metadata.get("prompt_tokens"),
                    "completion_tokens": metadata.get("completion_tokens"),
                    "total_tokens": metadata.get("total_tokens"),
                    "content": run["content"],
                }
            )

    write_svg_bar_chart(counts, RESULTS_DIR / "self_consistency.svg")

    print("\n=== Direct answer ===")
    print(direct["content"])
    print("Metadata:", direct["metadata"])

    print("\n=== Zero-shot Chain-of-Thought ===")
    print(cot["content"])
    print("Metadata:", cot["metadata"])

    print("\n=== Self-consistency answer counts ===")
    for answer, count in counts.most_common():
        print(f"{answer}: {count}")

    print("\nSaved:")
    print("  results/reasoning_experiment.json")
    print("  results/reasoning_experiment.csv")
    print("  results/self_consistency.svg")


if __name__ == "__main__":
    main()
