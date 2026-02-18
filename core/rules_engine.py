from __future__ import annotations
import pandas as pd
import yaml
from typing import Dict, Any

def load_traits() -> Dict[str, Any]:
    with open("data/pwf_traits.yml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_templates() -> Dict[str, Any]:
    with open("data/card_templates.yml", "r", encoding="utf-8") as f:
        templates = yaml.safe_load(f)
    return {t["template_id"]: t for t in templates}

def load_rules() -> pd.DataFrame:
    return pd.read_csv("data/rules.csv")

def render_card(template: Dict[str, str], power: Dict[str, str], watch: Dict[str, str], fuel: Dict[str, str]) -> Dict[str, str]:
    return {
        "power": template["power_block"].format(power_label=power["label"], power_micro_move=power["micro_move"]),
        "watch": template["watch_block"].format(watch_label=watch["label"], watch_micro_move=watch["micro_move"]),
        "fuel": template["fuel_block"].format(fuel_label=fuel["label"], fuel_micro_move=fuel["micro_move"]),
    }

def generate_card(priority_path: str, stakes: str, profile: Dict[str, Any]) -> Dict[str, Any]:
    traits = load_traits()
    templates = load_templates()
    rules = load_rules()

    # Match rules for this priority path and stakes
    candidates = rules[
        (rules["priority_path"] == priority_path) &
        ((rules["stakes"] == stakes) | (rules["stakes"] == "any"))
    ]

    if candidates.empty:
        # fallback: try any stakes
        candidates = rules[(rules["priority_path"] == priority_path) & (rules["stakes"] == "any")]

    if candidates.empty:
        raise ValueError(f"No rules found for priority_path='{priority_path}'")

    top = candidates.sort_values("weight", ascending=False).iloc[0]
    template = templates[top["template_id"]]

    power = next(x for x in traits["powers"] if x["id"] == profile["power_id"])
    watch = next(x for x in traits["watches"] if x["id"] == profile["watch_id"])
    fuel  = next(x for x in traits["fuels"]  if x["id"] == profile["fuel_id"])

    blocks = render_card(template, power, watch, fuel)
    return {"priority_path": priority_path, "stakes": stakes, "blocks": blocks, "template_id": top["template_id"]}
