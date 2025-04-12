import os

from ai_assistant_tester.prompts import format_knowledge_base_chunk


def get_openai_api_key() -> str:
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise EnvironmentError("Please set the OPENAI_API_KEY environment variable.")
    return OPENAI_API_KEY


def send_to_openai(
    prompt: str, extracted_text: str, model: str = "gpt-4o", temperature: float = 0.0
):
    pass
