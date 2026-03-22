import json
import os

_rules_cache = None


def load_rules():
    """Read the rules file and return the parsed JSON. Caches result so file is only opened once."""
    global _rules_cache
    if _rules_cache is None:
        filename = os.path.join(os.path.dirname(__file__), "plastic_rules.json")
        with open(filename, "r", encoding="utf-8") as fp:
            _rules_cache = json.load(fp)
    return _rules_cache


def analyze_plastic(plastic_type):
    rules = load_rules()

    if plastic_type not in rules:
        return {
            "status": "unknown",
            "message": "Plastic type not recognized. Avoid reuse for safety."
        }

    plastic = rules[plastic_type]

    if plastic["reusable"]:
        decision = "Reusable"
    elif plastic["recyclable"]:
        decision = "Recyclable (Not Reusable)"
    else:
        decision = "Single-use / Avoid Reuse"

    return {
        "plastic_type": plastic_type,
        "decision": decision,
        "explanation": plastic["explanation"]
    }