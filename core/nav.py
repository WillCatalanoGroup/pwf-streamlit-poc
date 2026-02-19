from __future__ import annotations

import json
from pathlib import Path
import streamlit as st
import yaml


STORAGE_DIR = Path("storage")


def get_user_id() -> str:
    return str(st.session_state.get("user_id", "")).strip()


def set_user_id(user_id: str) -> None:
    st.session_state["user_id"] = str(user_id).strip()


def user_path(user_id: str) -> Path:
    return STORAGE_DIR / f"{user_id}.json"


def init_user_if_missing(user_id: str) -> None:
    """
    Creates storage/<user_id>.json if missing.
    Writes a minimal shape plus a default profile so other pages do not crash.
    """
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    p = user_path(user_id)
    if p.exists():
        return

    # Default trait ids (first item in each list) so app can run before V2 profile pages exist.
    traits = yaml.safe_load(open("data/pwf_traits.yml", "r", encoding="utf-8"))
    power_id = traits["powers"][0]["id"]
    watch_id = traits["watches"][0]["id"]
    fuel_id  = traits["fuels"][0]["id"]

    doc = {
        "user_id": user_id,
        # Legacy-compatible single ids (current engine expects these)
        "profile": {"power_id": power_id, "watch_id": watch_id, "fuel_id": fuel_id},
        "history": [],
    }
    p.write_text(json.dumps(doc, indent=2), encoding="utf-8")


def require_user_id_or_redirect() -> None:
    """
    If user_id is missing, redirect back to onboarding.
    """
    if not get_user_id():
        st.switch_page("pages/1_Onboarding.py")
