import json
import re
import statistics
from pathlib import Path
from pprint import pprint
from typing import Dict, List

from ai_assistant_tester.assistant_manager.AssistantManager import AssistantManager
from ai_assistant_tester.conversation_tester.AssistantTestSession import (
    AssistantTestSession,
)
from ai_assistant_tester.prompts import system_answer_evaluation
from ai_assistant_tester.utils.constants import KNOWLEDGE_BASE_OUTPUTS_DIR
from ai_assistant_tester.utils.utils import QAPairs, load_json_file_qa_pairs


class AssistantEvaluator:
    def __init__(self, assistant_manager: AssistantManager):
        self.manager = assistant_manager

    def _build_items(self, qa_pairs: QAPairs, answers: List[str]) -> list[dict]:
        items: list[dict] = []
        for idx, qa in enumerate(qa_pairs["qas"]):
            items.append(
                {
                    "index": idx + 1,
                    "question": qa["question"],
                    "reference": qa["answer"].strip(),
                    "actual": answers[idx] if idx < len(answers) else "",
                }
            )
        return items

    def _build_user_eval_prompt(self, items: list[dict]) -> str:
        """
        items = [
            {"index": 1, "question": "...", "reference": "...", "actual": "..."},
            …
        ]
        """
        items_json = json.dumps(items, indent=2, ensure_ascii=False)
        return (
            "Evaluate the following items and return ONLY the JSON array described above:\n\n"
            f"{items_json}"
        )

    def _strip_code_fences(self, text: str) -> str:
        """Remove ```json … ``` or ``` … ``` blocks around the payload, if present for safe json parsing."""
        return re.sub(r"^\s*```(?:json)?\s*([\s\S]*?)\s*```\s*$", r"\1", text.strip())

    def evaluate(
        self,
        qa_pairs: QAPairs,
        answers: List[str],
        model: str = "gpt-4o-mini",
    ) -> List[Dict]:
        """Returns merged grading rows (question, reference, actual, verdict …)."""
        items = self._build_items(qa_pairs, answers)
        user_prompt = self._build_user_eval_prompt(items)

        resp = self.manager.run_evaluation(
            system_content=system_answer_evaluation,
            user_content=user_prompt,
            model=model,
        )

        content = resp.choices[0].message.content or ""
        if not content.strip():
            raise ValueError("LLM evaluation response was empty")

        cleaned = self._strip_code_fences(content)

        try:
            grades = json.loads(cleaned)
            if not isinstance(grades, list):
                raise ValueError("Top‑level JSON is not a list")
        except Exception as e:
            # fall back: mark every item as parse‑error
            grades = [
                {
                    "index": itm["index"],
                    "verdict": "ParseError",
                    "score": 0.0,
                    "notes": f"Could not parse evaluator response ({e})",
                }
                for itm in items
            ]

        # merge evaluator verdict with original Q/A data
        merged: List[Dict] = []
        grade_dict = {g["index"]: g for g in grades}  # quick lookup
        for itm in items:
            g = grade_dict.get(itm["index"], {})
            merged.append(
                {
                    **itm,  # question / reference / actual
                    "verdict": g.get("verdict", "Missing"),
                    "score": g.get("score", 0.0),
                    "notes": g.get("notes", ""),
                }
            )
        return merged

    # ---------------------------------------------------------------------------

    @staticmethod
    def generate_report(rows: List[Dict]) -> str:
        """Return a Markdown summary (totals + table)."""
        total = len(rows)
        avg_score = statistics.mean(r["score"] for r in rows) if rows else 0.0
        correct = sum(1 for r in rows if r["verdict"] == "Correct")
        partial = sum(1 for r in rows if r["verdict"] == "Partial")
        incorrect = sum(1 for r in rows if r["verdict"] == "Incorrect")

        header = (
            f"# Evaluation Report\n\n"
            f"* **Total questions:** {total}\n"
            f"* **Average score:** {avg_score:.2f}\n"
            f"* **Correct / Partial / Incorrect:** "
            f"{correct} / {partial} / {incorrect}\n\n"
        )

        table_header = (
            "| # | Verdict | Score | Question | Notes |\n"
            "|---|---------|-------|----------|-------|\n"
        )

        rows_md = "\n".join(
            f"| {r['index']} | {r['verdict']} | {r['score']:.1f} | "
            f"{r['question']} | {r['notes'].replace('|','\\|')} |"
            for r in rows
        )

        return header + table_header + rows_md


if __name__ == "__main__":
    from ai_assistant_tester.conversation_tester.AssistantTestSession import (
        AssistantTestSession,
    )
    from ai_assistant_tester.utils.constants import KNOWLEDGE_BASE_OUTPUTS_DIR
    from ai_assistant_tester.utils.utils import load_json_file_qa_pairs

    qa_pairs = load_json_file_qa_pairs("./qa_set.json")
    mgr = AssistantManager()
    session = AssistantTestSession(
        name="QA Tester",
        instructions="You are a helpful assistant. Answer each numbered question clearly.",
        tools=[{"type": "file_search"}],
        model="gpt-4o-mini",
        kb_file=KNOWLEDGE_BASE_OUTPUTS_DIR / "example.md",
        manager=mgr,
    )

    answers = session.run_test(qa_pairs)
    print("Assistant answers:", answers)

    evaluator = AssistantEvaluator(mgr)
    graded_rows = evaluator.evaluate(qa_pairs, answers)
    pprint(graded_rows)

    md_report = evaluator.generate_report(graded_rows)
    Path("evaluation_report.md").write_text(md_report, encoding="utf-8")
    print("\nMarkdown report written to evaluation_report.md")
