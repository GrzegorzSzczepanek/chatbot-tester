import json
import os
from pathlib import Path
from typing import List, TypedDict

from openai import OpenAI


def get_openai_api_key() -> str:
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise EnvironmentError("Please set the OPENAI_API_KEY environment variable.")
    return OPENAI_API_KEY


def get_file_content(file_path: Path) -> str:
    with open(file_path, "r") as file:
        return file.read()


def get_client() -> OpenAI:
    client = OpenAI(api_key=get_openai_api_key())
    return client


def knowledge_base_content(file_path: Path) -> str:
    content = get_file_content(file_path)
    return content


class QAPair(TypedDict):
    question: str
    answer: str


class QAPairs(TypedDict):
    qas: List[QAPair]


def load_json_file_qa_pairs(filepath: str) -> QAPairs:
    """
    Load and validate QA pairs from a JSON file.
    """
    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"File {filepath} not found")
    data = json.loads(path.read_text())
    if (
        not isinstance(data, dict)
        or "qas" not in data
        or not isinstance(data["qas"], list)
    ):
        raise ValueError(f"Invalid QA pairs structure in {filepath}")
    for item in data["qas"]:
        if not (
            isinstance(item, dict)
            and isinstance(item.get("question"), str)
            and isinstance(item.get("answer"), str)
        ):
            raise ValueError(
                "Each QA item must be a dict with 'question' and 'answer' strings"
            )
    return data  # type: ignore
