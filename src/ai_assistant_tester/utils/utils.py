import os

from openai import OpenAI

from ai_assistant_tester.prompts import format_knowledge_base_chunk


def get_openai_api_key() -> str:
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise EnvironmentError("Please set the OPENAI_API_KEY environment variable.")
    return OPENAI_API_KEY


def get_file_content(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()


def get_client() -> OpenAI:
    client = OpenAI(api_key=get_openai_api_key())
    return client
