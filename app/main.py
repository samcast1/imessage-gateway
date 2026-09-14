from fastapi import FastAPI
from pydantic import BaseModel

from app.agent import run_agent


app = FastAPI(title="iMessage Gateway")


class Command(BaseModel):
    command: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/command")
def command(payload: Command):
    try:
        response = run_agent(payload.command)

        return {
            "success": True,
            "response": response,
        }

    except Exception as e:
        return {
            "success": False,
            "response": f"Agent failed: {e}",
        }