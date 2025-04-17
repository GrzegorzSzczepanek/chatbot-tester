from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

KNOWLEDGE_BASE_OUTPUTS_DIR = (
    PROJECT_ROOT / "ai_assistant_tester" / "knowledge_base" / "outputs"
)

QA_PAIRS_DIR = PROJECT_ROOT / "ai_assistant_tester" / "knowledge_base" / "qa_pairs"
