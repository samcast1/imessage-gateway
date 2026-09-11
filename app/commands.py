# app/commands.py

from app.whoop import run_whoop


def hello():
    return "hello handsome"


def whoop_morning():
    return run_whoop("morning")


def whoop_evening():
    return run_whoop("evening")


COMMANDS = {
    "hello": hello,
    "whoop morning": whoop_morning,
    "whoop evening": whoop_evening,
}