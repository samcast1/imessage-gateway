# app/whoop.py

import os
import requests

WHOOP_API_URL = os.environ["WHOOP_API"]


def run_whoop(mode: str) -> str:
    response = requests.post(
        f"{WHOOP_API_URL}/{mode}",
        timeout=90,
    )

    response.raise_for_status()

    return response.json()["message"]