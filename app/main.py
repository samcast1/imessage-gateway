from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="iMessage Gateway")


class Command(BaseModel):
    command: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/command")
def command(payload: Command):
    command = payload.command.strip().lower()

    if command == "hello":
        return {
            "success": True,
            "response": "hello handsome"
        }

    return {
        "success": False,
        "response": f"I don't know how to handle: {command}"
    }