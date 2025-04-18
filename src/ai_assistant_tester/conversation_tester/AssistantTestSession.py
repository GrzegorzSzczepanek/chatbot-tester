import re
import time
from pathlib import Path
from pprint import pprint
from typing import Any, List, Optional

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
        manager: AssistantManager,
        model: str = "gpt-4o",
        kb_file: Optional[Path] = None,
    ):
        self.kb_formatter = KnowledgeBaseFormatter(model=model)
        self.manager = manager

        if kb_file:
            vector_store_id = manager.add_vector_stores(
                name="knowledge base",
                filepaths=[kb_file],
            )
            self.tool_resources = {
                "file_search": {"vector_store_ids": [vector_store_id]}
            }
        else:
            self.tool_resources = None

        self.assistant = self.manager.create_assistant(
            name=name,
            instructions=instructions,
            tools=tools,
            model=model,
            tool_resources=self.tool_resources,
        )

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
            print(f"Run status: {run.status}")

            if run.status == "requires_action":
                print("Assistant is trying to use tools!")
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

    def _parse_numbered_answers(self, reply: str) -> List[str]:
        pattern = r"(?:\*\*)?(\d+)\.(?:\*\*)?\s*(.*?)(?=\s*(?:\*\*\d+\.|$))"
        matches = re.findall(pattern, reply, flags=re.DOTALL)
        return [m[1].strip() for m in matches]

    def run_test(self, qa_pairs: QAPairs) -> List[str]:
        answers = []
        for qa in qa_pairs["qas"]:
            thread = self.manager.create_thread()
            self.manager.add_message(thread, "user", qa["question"])
            run = self.manager.create_run(thread.id, self.assistant.id)
            self._wait_for_run(thread.id, run.id)
            answers.append(self._extract_assistant_response(thread.id))
        return answers


# if __name__ == "__main__":
#     qa_pairs = load_json_file_qa_pairs("./qa_set.json")
#     session = AssistantTestSession(
#         name="QA Tester",
#         instructions="You are a helpful assistant. Answer each numbered question clearly.",
#         tools=[{"type": "file_search"}],
#         model="gpt-4o-mini",
#         kb_file=KNOWLEDGE_BASE_OUTPUTS_DIR / "example.md",
#     )
#     answers = session.run_test(qa_pairs)
#     print("Assistant answers:", answers)
