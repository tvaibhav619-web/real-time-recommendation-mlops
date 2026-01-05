import json
from pathlib import Path

LOG_PATH = Path("evaluation/logged_events.jsonl")
LOG_PATH.parent.mkdir(exist_ok=True)

def log_event(event: dict):
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(event) + "\n")
