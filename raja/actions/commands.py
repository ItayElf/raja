import difflib
from typing import List

from raja.actions import init, add, config
from raja.utils import error

_commands = {
    "init": init.init,
    "destroy": init.destroy,
    "add": add.add,
    "remove": add.remove,
    "config": config.config,
}


def handle_command(cmd: str, parans: List[str]) -> None:
    """Calls a command based on its name and the given parameters"""
    if cmd not in _commands:
        error(f"Illegal command: '{cmd}'")
        closest_matches_str = "\n\t".join(difflib.get_close_matches(cmd, _commands.keys()))
        if closest_matches_str:
            print(f"Similar commands: \n\t{closest_matches_str}")
        return
    try:
        _commands[cmd](*parans)
    except TypeError:
        error(f"Illegal number of arguments to command {cmd}.")
    # except Exception as e:
    #     print(e)
