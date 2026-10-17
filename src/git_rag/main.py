from fastapi import FastAPI
from git_rag.service import ask_repository
from pydantic import BaseModel, HttpUrl

app = FastAPI(title="Ask Your Repository")

@app.get("/")
def home():
    return {"message":"Ask your Repository"}

@app.get("/health")
def health_check():
    return {"status":"ok"}


from pydantic import BaseModel

class AskRequest(BaseModel):
    repo_url: HttpUrl
    question: str


@app.post("/ask")
def ask_endpoint(request: AskRequest):
    return ask_repository(str(request.repo_url), request.question)

