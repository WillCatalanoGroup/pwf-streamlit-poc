import json
from pathlib import Path
from typing import Any, Dict

STORAGE_DIR = Path("storage")
STORAGE_DIR.mkdir(exist_ok=True)

def _path(user_id: str) -> Path:
    return STORAGE_DIR / f"{user_id}.json"

def load_user(user_id: str) -> Dict[str, Any]:
    p = _path(user_id)
    if not p.exists():
        return {"user_id": user_id, "profile": {}, "history": []}
    return json.loads(p.read_text(encoding="utf-8"))

def save_user(user: Dict[str, Any]) -> None:
    p = _path(user["user_id"])
    p.write_text(json.dumps(user, indent=2), encoding="utf-8")
