import boto3
import os
from dotenv import load_dotenv

load_dotenv()

MODEL_ID = "amazon.nova-lite-v1:0"
REGION = os.getenv("AWS_REGION", "ap-southeast-2")


def generate_answer(question: str, matches: list[dict]) -> str:
    sources = []

    for number, chunk in enumerate(matches, start=1):
        sources.append(
            f"[Source {number}: {chunk['path']}:{chunk['start_line']}-{chunk['end_line']}]\n"
            f"{chunk['text']}"
        )

    context = "\n\n".join(sources)

    client = boto3.client("bedrock-runtime", region_name=REGION)
    response = client.converse(
        modelId=MODEL_ID,
        system=[{
            "text": (
                "Answer the user's question using only the supplied repository "
                "passages. If they do not contain the answer, say you could not "
                "find it in the repository. Cite claims using the source labels."
            )
        }],
        messages=[{
            "role": "user",
            "content": [{
                "text": f"Question: {question}\n\nRepository passages:\n{context}"
            }],
        }],
        inferenceConfig={"maxTokens": 400, "temperature": 0.2},
    )

    return response["output"]["message"]["content"][0]["text"]