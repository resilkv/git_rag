# Git RAG

Git RAG is a small FastAPI application that answers questions using files in the
current repository. It reads supported text files, splits them into overlapping
line-based chunks, embeds the chunks with Amazon Bedrock, retrieves the closest
matches for a question, and asks a Bedrock model to answer using those passages.

## Requirements

- Python 3.12 or later
- [uv](https://docs.astral.sh/uv/)
- AWS credentials available through the [Boto3 credential provider chain](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html)
- Amazon Bedrock access in your selected AWS region for:
  - `amazon.titan-embed-text-v2:0` (embeddings)
  - `amazon.nova-lite-v1:0` (answer generation)

The default AWS region is `ap-southeast-2`. Override it by setting `AWS_REGION`
in your environment or in a `.env` file in the working directory. Do not commit
AWS credentials to the repository.

## Setup

Install the project and its dependencies:

```bash
uv sync
```

On some macOS Python installations, Python skips the hidden `.pth` file used by
uv's editable install, which makes `git_rag` imports fail. If that happens,
install the project as a regular wheel instead:

```bash
export UV_NO_EDITABLE=1
uv sync --reinstall-package git-rag
```

Keep `UV_NO_EDITABLE=1` set for subsequent uv commands so a later sync does not
switch back to an editable installation.

## Run the API

Start the development server from the repository root:

```bash
uv run fastapi dev src/git_rag/main.py
```

The API is available at `http://127.0.0.1:8000`. FastAPI's interactive API
documentation is at `http://127.0.0.1:8000/docs`.

### Endpoints

- `GET /` returns a welcome message.
- `GET /health` returns the service health status.
- `POST /ask` accepts a JSON question and returns an answer.

Example:

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H 'Content-Type: application/json' \
  -d '{"question":"How does this app create text embeddings?"}'
```

The answer is generated from retrieved repository passages and includes source
labels with file paths and line ranges. The response shape is:

```json
{"answer":"..."}
```

## Indexing behavior

The repository reader includes `.py`, `.md`, `.toml`, `.yaml`, `.yml`, and
`.json` files. It skips `.git`, `.venv`, `__pycache__`, `build`, `dist`, and
`*.egg-info` directories. Files are split into chunks of 40 lines with 8 lines
of overlap.

The first `/ask` request builds an index for the process's current working
directory; that index is cached for later requests in the same process. The
current index keeps all discovered chunks, so embedding a large repository can
make many Bedrock requests. Each question also requires an embedding request and
an answer-generation request. These calls may incur AWS charges.