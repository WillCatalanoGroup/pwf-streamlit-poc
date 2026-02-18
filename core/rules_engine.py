from __future__ import annotations

import csv
from typing import Dict, Any

import pandas as pd
import yaml


def load_traits() -> Dict[str, Any]:
    with open("data/pwf_traits.yml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_templates() -> Dict[str, Any]:
    # Base templates
    with open("data/card_templates.yml", "r", encoding="utf-8") as f:
        base = yaml.safe_load(f) or []
    merged = {t["template_id"]: t for t in base}

    # Optional overrides/additions
    try:
        with open("data/card_templates_custom.yml", "r", encoding="utf-8") as f:
            custom = yaml.safe_load(f) or []
        for t in custom:
            merged[t["template_id"]] = t
    except FileNotFoundError:
        pass

    return merged


def load_rules() -> pd.DataFrame:
    return pd.read_csv("data/rules.csv")


def render_card(
    template: Dict[str, str],
    power: Dict[str, str],
    watch: Dict[str, str],
    fuel: Dict[str, str],
) -> Dict[str, str]:
    return {
        "power": template["power_block"].format(
            power_label=power["label"],
            power_micro_move=power["micro_move"],
        ),
        "watch": template["watch_block"].format(
            watch_label=watch["label"],
            watch_micro_move=watch["micro_move"],
        ),
        "fuel": template["fuel_block"].format(
            fuel_label=fuel["label"],
            fuel_micro_move=fuel["micro_move"],
        ),
    }


def generate_card(priority_path: str, stakes: str, profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    priority_path is treated as a stable key (for example: 'meetings > lead').
    stakes is one of: low, medium, high.
    """
    traits = load_traits()
    templates = load_templates()
    rules = load_rules()

    # 1) Exact key match
    candidates = rules[
        (rules["priority_path"] == priority_path)
        & ((rules["stakes"] == stakes) | (rules["stakes"] == "any"))
    ]

    # 2) Any fallback in rules.csv
    if candidates.empty:
        candidates = rules[
            (rules["priority_path"] == "any")
            & ((rules["stakes"] == stakes) | (rules["stakes"] == "any"))
        ]

    # 3) Hard fallback
    if candidates.empty:
        template_id = "generic_any_priority"
    else:
        top = candidates.sort_values("weight", ascending=False).iloc[0]
        template_id = str(top["template_id"])

    if template_id not in templates:
        template_id = "generic_any_priority"

    template = templates[template_id]

    power = next(x for x in traits["powers"] if x["id"] == profile["power_id"])
    watch = next(x for x in traits["watches"] if x["id"] == profile["watch_id"])
    fuel = next(x for x in traits["fuels"] if x["id"] == profile["fuel_id"])

    blocks = render_card(template, power, watch, fuel)

    return {
        "priority_path": priority_path,
        "stakes": stakes,
        "template_id": template_id,
        "blocks": blocks,
    }
