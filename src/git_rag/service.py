from functools import lru_cache
from pathlib import Path
from tempfile import TemporaryDirectory



from git_rag.generation import generate_answer
from git_rag.git_source import clone_public_github_repo
from git_rag.indexing import build_index
from git_rag.retrieval import retrieve



@lru_cache(maxsize=4)
def get_index(repo_url: str) -> list[dict]:
    # Clone into a temporary folder. The index keeps the text and vectors
    # in memory after the temporary checkout is deleted.
    with TemporaryDirectory(prefix="git-rag-") as temp_dir:
        repo_path = Path(temp_dir) / "repo"
        clone_public_github_repo(repo_url, repo_path)
        return build_index(repo_path, max_chunks=20)



def ask_repository(repo_url: str, question: str) -> dict:
    matches = retrieve(get_index(repo_url), question)
    answer = generate_answer(question, matches)

    sources = [
        {
            "path": match["path"],
            "start_line": match["start_line"],
            "end_line": match["end_line"],
        }
        for match in matches
    ]

    return {"answer": answer, "sources": sources}