import difflib
import json
import os

from raja.utils import error, success

_allowed_settings = {
    "username",
    "base_url",
}


def config(setting: str, value: str) -> None:
    """Changes a setting of the raja workspace"""
    if not os.path.isdir(".raja"):
        error("Raja was not initialized. Use 'raja init'")
        return
    if setting not in _allowed_settings:
        error(f"Illegal setting: {setting}.")
        closest_matches_str = "\n\t".join(difflib.get_close_matches(setting, _allowed_settings))
        if closest_matches_str:
            print(f"Similar settings: \n\t{closest_matches_str}")
        return
    with open(os.path.join(".raja", ".raja_settings.json")) as f:
        settings = json.load(f)
    settings[setting] = value
    with open(os.path.join(".raja", ".raja_settings.json"), "w") as f:
        json.dump(settings, f, indent=2)
    success(f"{setting.title()} changed successfully to '{value}'")
