import tiktoken
from openai import OpenAI

from ai_assistant_tester.utils.utils import get_file_content, get_openai_api_key

messages = [
    {
        "role": "system",
        "content": "You will help format a long knowledge base in small parts. Each part continues the previous one. Maintain coherence and don't repeat what has been said.",
    }
]

model = "gpt-4o"
max_tokens_per_chunk = 1000
client = OpenAI(api_key=get_openai_api_key())
encoding = tiktoken.encoding_for_model(model)
temperature = 0.0


def generate_question_answer_set(filepath: str) -> None:
    file = get_file_content("example.md")
