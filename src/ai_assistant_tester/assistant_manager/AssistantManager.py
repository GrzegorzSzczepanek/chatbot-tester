from typing import Literal

from openai import OpenAI
from openai.pagination import SyncCursorPage
from openai.types.beta import ThreadDeleted, assistant
from openai.types.beta.assistant import Assistant
from openai.types.beta.thread import Thread
from openai.types.beta.thread_create_and_run_params import Tool
from openai.types.beta.threads.message import Message
from openai.types.beta.threads.run import Run
from openai.types.beta.threads.run_submit_tool_outputs_params import ToolOutput
from openai.types.beta.threads.runs.run_step import RunStep
from openai.types.chat.chat_completion import ChatCompletion

from ai_assistant_tester.utils.utils import get_client


class AssistantManager:
    def __init__(self) -> None:
        self.client = get_client()

    def get_client(self) -> OpenAI:
        return self.client

    def create_thread(self) -> Thread:
        thread = self.client.beta.threads.create()
        return thread

    def retrieve_thread(self, thread_id: str) -> Thread:
        thread = self.client.beta.threads.retrieve(thread_id)
        return thread

    def delete_thread(self, thread_id: str) -> ThreadDeleted:
        response = self.client.beta.threads.delete(thread_id)
        return response

    def add_message(
        self,
        thread: Thread,
        role: Literal["user", "assistant"],
        content: str,
    ) -> Message:
        message = self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role=role,
            content=content,
        )
        return message

    def list_runs(self, assistant_id: str) -> SyncCursorPage[Run]:
        runs = self.client.beta.threads.runs.list(assistant_id)
        return runs

    def retrieve_run(self, thread_id: str, run_id: str) -> Run:
        run = self.client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        return run

    def update_thread(
        self, thread_id: str, run_id: str, metadata: dict[str, str]
    ) -> Run:
        run = self.client.beta.threads.runs.update(
            thread_id=thread_id, run_id=run_id, metadata=metadata
        )
        return run

    def submit_run(
        self, thread_id: str, run_id: str, tool_outputs: list[ToolOutput]
    ) -> Run:
        run = self.client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread_id,
            run_id=run_id,
            tool_outputs=tool_outputs,
        )
        return run

    def cancel_run(self, thread_id: str, run_id: str) -> Run:
        run = self.client.beta.threads.runs.cancel(thread_id=thread_id, run_id=run_id)
        return run

    def get_run_steps(self, thread_id: str, run_id: str) -> SyncCursorPage[RunStep]:
        run_steps = self.client.beta.threads.runs.steps.list(
            thread_id=thread_id, run_id=run_id
        )
        return run_steps

    def get_run_step(self, thread_id: str, run_id: str, step_id: str) -> RunStep:
        run_step = self.client.beta.threads.runs.steps.retrieve(
            thread_id=thread_id, run_id=run_id, step_id=step_id
        )
        return run_step

    def retrieve_message(self, thread_id: str, message_id: str) -> Message:
        message = self.client.beta.threads.messages.retrieve(
            message_id=message_id, thread_id=thread_id
        )
        return message

    def get_thread_messages(self, thread_id: str) -> SyncCursorPage:
        thread_messages = self.client.beta.threads.messages.list(thread_id)
        return thread_messages

    def create_run(self, thread_id: str, assistant_id: str) -> Run:
        run = self.client.beta.threads.runs.create(
            thread_id=thread_id, assistant_id=assistant_id
        )
        return run

    def create_thread_and_run(self, assistant_id: str, messages: SyncCursorPage):
        run = self.client.beta.threads.create_and_run(
            assistant_id=assistant_id, thread={"messages": messages}
        )

        return run

    def connect(self, assistant_id: str) -> Assistant:
        assistant = self.client.beta.assistants.retrieve(assistant_id)
        return assistant

    def create_assistant(
        self, name: str, instructions: str, tools: list[Tool], model: str
    ) -> Assistant:
        assistant = self.client.beta.assistants.create(
            name=name, instructions=instructions, tools=tools, model=model
        )
        return assistant

    def update_assistant(
        self,
        assistant_id: str,
        instructions: str,
        name: str,
        tools: list[Tool],
        model: str = "gpt-4o",
    ):
        updated_assistant = self.client.beta.assistants.update(
            assistant_id, instructions=instructions, name=name, tools=tools, model=model
        )

        return updated_assistant

    def delete_assistant(self, assistant_id: str) -> None:
        response = self.client.beta.assistants.delete(assistant_id)
        print(response)

    def run_evaluation(
        self, system_content: str, user_content: str, model: str = "gpt-4o-mini"
    ) -> ChatCompletion:
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content},
            ],
        )
        return response
