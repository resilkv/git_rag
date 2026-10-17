from pathlib import Path

ALLOWED_SUFFIXES = {
    ".py",
    ".md",
    ".toml",
    ".yaml",
    ".yml",
    ".json",
}

def read_repository(root: Path) -> list[tuple[str,str]]:
    document = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue

        excluded_dirs = {".git", ".venv", "__pycache__", "build", "dist"}

        if any(
            part in excluded_dirs or part.endswith(".egg-info")
            for part in path.relative_to(root).parts
        ):
            continue

        if path.suffix not in ALLOWED_SUFFIXES:
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError,OSError):
            continue

        relative_path = str(path.relative_to(root))
        document.append((relative_path,text))

    return document

def chunk_document(path: str , text: str, chunk_size: int = 40, overlap: int= 8) -> list[dict[str,str | int]]:

    lines = text.splitlines()
    chunks =[]
    start = 0

    while start<len(lines):
        end = min(start+chunk_size,len(lines))
        chunk_text = "\n".join(lines[start:end])
        chunks.append(
            {
                "path": path,
                "start_line": start+1,
                "end_line": end,
                "text" : chunk_text

            }
        )
        if end == len(lines):
            break
        start = end - overlap

    return chunks