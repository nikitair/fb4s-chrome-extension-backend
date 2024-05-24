import json
import os.path

from config import ROOT_DIR
from config.logging_config import logger

SIGNATURES_JSON_PATH = os.path.join(ROOT_DIR, "database", "signatures.json")


def get_signature(team_member_id: int):
    team_member_signature = "\n\nFB4S Team"
    try:
        with open(SIGNATURES_JSON_PATH, "r") as f:
            all_signatures = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logger.error(f"!!! FILE NOT FOUND - {SIGNATURES_JSON_PATH}")
        all_signatures = []

    for signature in all_signatures:
        if signature.get("fub_id") == team_member_id:
            team_member_signature = signature.get("signature")
            break
    return team_member_signature
