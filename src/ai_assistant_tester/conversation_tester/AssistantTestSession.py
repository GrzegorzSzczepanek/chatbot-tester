import json
import re
import time
from pathlib import Path
from pprint import pprint
from typing import Any, List, Optional, TypedDict

from openai.types.beta.thread_create_and_run_params import Tool

from ai_assistant_tester.assistant_manager.AssistantManager import AssistantManager
from ai_assistant_tester.knowledge_base.KnowledgeBaseFormatter import (
    KnowledgeBaseFormatter,
)
from ai_assistant_tester.utils.constants import KNOWLEDGE_BASE_OUTPUTS_DIR
from ai_assistant_tester.utils.utils import QAPair, QAPairs, load_json_file_qa_pairs


class AssistantTestSession:
    """
    Encapsulates the flow: create assistant, optionally inject knowledge base,
    send QA batch, wait for numbered answer response, parse and evaluate.
    """

    def __init__(
        self,
        name: str,
        instructions: str,
        tools: List[Tool],
        model: str = "gpt-4o-mini",
        kb_file: Optional[Path] = None,
    ):
        self.kb_formatter = KnowledgeBaseFormatter(model=model)
        self.manager = AssistantManager()
        self.assistant = self.manager.create_assistant(
            name=name,
            instructions=instructions,
            tools=tools,
            model=model,
        )
        self.kb_file = kb_file

    def _format_question_batch(self, qa_set: List[QAPair]) -> str:
        """
        Build a numbered list of questions for structured response from the assistant.
        """
        return "\n".join(f"{i+1}. {qa['question']}" for i, qa in enumerate(qa_set))

    def _wait_for_run(self, thread_id: str, run_id: str, timeout: float = 60.0) -> None:
        """
        Polls the run status until completion or timeout.
        """
        start = time.time()
        while True:
            run = self.manager.retrieve_run(thread_id, run_id)
            if run.status == "completed":
                return
            if time.time() - start > timeout:
                raise TimeoutError("Assistant did not complete run in time")
            time.sleep(0.5)

    def _extract_assistant_response(self, thread_id: str) -> str:
        """
        Retrieves the latest assistant message content from the thread.
        """
        messages = self.manager.get_thread_messages(thread_id)
        for msg in reversed(messages.data):
            if msg.role == "assistant":
                return msg.content[0].text.value
        raise RuntimeError("No assistant response found in thread")

    def _parse_numbered_answers(self, reply: str, expected_count: int) -> List[str]:
        """
        Parses a numbered list reply into individual answers.
        """
        pattern = re.compile(r"^\s*(\d+)\.\s*(.*)$", flags=re.MULTILINE)
        answers = []
        for match in pattern.finditer(reply):
            answers.append(match.group(2).strip())
        # If fewer answers than expected, pad with empty strings
        while len(answers) < expected_count:
            answers.append("")
        return answers

    def run_test(self, qa_pairs: QAPairs) -> List[str]:
        """
        Runs the QA session: optionally inject KB, send questions, wait, and return parsed answers.
        """
        qa_set = qa_pairs["qas"]
        thread = self.manager.create_thread()
        thread_id = thread.id

        # Inject knowledge base context at start of conversation
        if self.kb_file:
            kb_path = Path(self.kb_file)
            if not kb_path.is_file():
                raise FileNotFoundError(f"KB file {self.kb_file} not found")
            kb_text = kb_path.read_text()
            self.manager.add_message(
                thread=thread,
                role="user",
                content=f"### Reference Material:\n{kb_text}",
            )

        batch_prompt = self._format_question_batch(qa_set)
        self.manager.add_message(thread=thread, role="user", content=batch_prompt)

        run = self.manager.create_run(thread_id, self.assistant.id)  # type: ignore
        self._wait_for_run(thread_id, run.id)  # type: ignore

        reply = self._extract_assistant_response(thread_id)

        return self._parse_numbered_answers(reply, expected_count=len(qa_set))

    def evaluate(
        self, qa_pairs: QAPairs, answers: List[str]
    ) -> List[dict[str, Optional[bool]]]:
        """
        Compares each expected answer to the assistant's parsed answers.
        Returns a list of verdict dicts.
        """
        verdicts = []
        for idx, qa in enumerate(qa_pairs["qas"]):
            expected = qa["answer"].strip()
            actual = answers[idx] if idx < len(answers) else ""
            correct = expected.lower() in actual.lower()
            verdicts.append(
                {
                    "question": qa["question"],
                    "expected": expected,
                    "actual": actual,
                    "correct": correct,
                }
            )
        return verdicts


if __name__ == "__main__":
    qa_pairs = load_json_file_qa_pairs("./qa_set.json")
    session = AssistantTestSession(
        name="QA Tester",
        instructions="You are a helpful assistant. Answer each numbered question clearly.",
        tools=[{"type": "file_search"}],
        model="gpt-4o-mini",
        kb_file=KNOWLEDGE_BASE_OUTPUTS_DIR / "example.md",
    )
    answers = session.run_test(qa_pairs)
    print("Assistant answers:", answers)
    results = session.evaluate(qa_pairs, answers)
    pprint(results)
