from pathlib import Path

from git_rag.embeddings import embed_text
from git_rag.repository import chunk_document, read_repository


def build_index(root: Path, max_chunks: int | None = None) -> list[dict]:
    index = []

    for path, text in read_repository(root):
        chunks = chunk_document(path, text)

        for chunk in chunks:
            if max_chunks is not None and len(index) >= max_chunks:
                return index

            index.append({
                **chunk,
                "embedding": embed_text(chunk["text"]),
            })

    return index