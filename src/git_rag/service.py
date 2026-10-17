from functools import lru_cache
from pathlib import Path

from git_rag.generation import generate_answer
from git_rag.indexing import build_index
from git_rag.retrieval import retrieve


@lru_cache(maxsize=1)
def get_index() -> list[dict]:
    # Limit the first version to three chunks to keep embedding requests small.
    return build_index(Path.cwd())


def ask_repository(question: str) -> str:
    matches = retrieve(get_index(), question)
    return generate_answer(question, matches)