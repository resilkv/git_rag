from git_rag.embeddings import embed_text


def retrieve(index: list[dict], question: str, top_k: int = 3) -> list[dict]:
    question_vector = embed_text(question)
    scored_chunks = []

    for chunk in index:
        chunk_vector = chunk["embedding"]
        score = sum(
            question_value * chunk_value
            for question_value, chunk_value in zip(
                question_vector, chunk_vector, strict=True
            )
        )

        scored_chunks.append({**chunk, "score": score})

    return sorted(
        scored_chunks,
        key=lambda chunk: chunk["score"],
        reverse=True,
    )[:top_k]