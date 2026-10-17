import json
import os

import boto3
from dotenv import load_dotenv

load_dotenv()

MODEL_ID = "amazon.titan-embed-text-v2:0"
REGION = os.getenv("AWS_REGION", "ap-southeast-2")


def embed_text(text: str) -> list[float]:
    if not text.strip():
        raise ValueError("Text to embed must not be empty")

    client = boto3.client("bedrock-runtime", region_name=REGION)

    response = client.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps({
            "inputText": text,
            "dimensions": 1024,
            "normalize": True,
        }),
    )

    result = json.loads(response["body"].read())
    return result["embedding"]