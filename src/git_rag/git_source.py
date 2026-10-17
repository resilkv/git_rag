import re
import subprocess
from pathlib import Path
from urllib.parse import urlsplit


def clone_public_github_repo(repo_url: str, destination: Path) -> None:
    parsed = urlsplit(repo_url)

    if (
        parsed.scheme != "https"
        or parsed.hostname != "github.com"
        or parsed.username
        or parsed.password
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError("Please provide a public HTTPS GitHub repository URL")

    parts = parsed.path.strip("/").split("/")
    if len(parts) != 2:
        raise ValueError("Use a repository URL like https://github.com/owner/repository")

    owner, repo = parts
    repo = repo.removesuffix(".git")

    valid_name = re.compile(r"[A-Za-z0-9_.-]+")
    if not valid_name.fullmatch(owner) or not valid_name.fullmatch(repo):
        raise ValueError("The GitHub owner or repository name is invalid")

    safe_url = f"https://github.com/{owner}/{repo}.git"

    subprocess.run(
        ["git", "clone", "--depth", "1", "--", safe_url, str(destination)],
        check=True,
        capture_output=True,
        text=True,
        timeout=120,
    )