from fastapi import FastAPI
from pydantic import BaseModel

from app.commands import COMMANDS

app = FastAPI(title="iMessage Gateway")


class Command(BaseModel):
    command: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/command")
def command(payload: Command):
    command = payload.command.strip().lower()

    handler = COMMANDS.get(command)

    if handler is None:
        return {
            "success": False,
            "response": f"I don't know how to handle: {command}",
        }

    try:
        response = handler()

        return {
            "success": True,
            "response": response,
        }

    except Exception as e:
        return {
            "success": False,
            "response": f"Command failed: {e}",
        }