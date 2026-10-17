from fastapi import FastAPI
from git_rag.service import ask_repository

app = FastAPI(title="Ask Your Repository")

@app.get("/")
def home():
    return {"message":"Ask your Repository"}

@app.get("/health")
def health_check():
    return {"status":"ok"}


from pydantic import BaseModel

class AskRequest(BaseModel):
    question:  str


@app.post("/ask")
def ask_endpoint(request: AskRequest):
    return {"answer": ask_repository(request.question)}

