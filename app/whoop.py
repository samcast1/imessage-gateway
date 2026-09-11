# app/whoop.py

import subprocess


WHOOP_DIR = "/opt/whoop-daily-sms"


def run_whoop(mode: str) -> str:
    result = subprocess.run(
        [
            "docker",
            "compose",
            "run",
            "--rm",
            "whoop-daily-sms",
            mode,
        ],
        cwd=WHOOP_DIR,
        capture_output=True,
        text=True,
        timeout=120,
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())

    return result.stdout.strip()