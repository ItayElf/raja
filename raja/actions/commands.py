import difflib
from typing import List

from raja.actions import init, add, config, commit, rollback
from raja.utils import error

_commands = {
    "init": init.init,
    "destroy": init.destroy,
    "reset": init.reset,
    "add": add.add,
    "remove": add.remove,
    "config": config.config,
    "commit": commit.commit,
    "rollback": rollback.rollback,
}  # test comment 2


def handle_command(cmd: str, params: List[str]) -> None:
    """Calls a command based on its name and the given parameters"""
    if cmd not in _commands:
        error(f"Illegal command: '{cmd}'")
        closest_matches_str = "\n\t".join(difflib.get_close_matches(cmd, _commands.keys()))
        if closest_matches_str:
            print(f"Similar commands: \n\t{closest_matches_str}")
        return
    # try:
    _commands[cmd](*params)  # test comment 1
    # except TypeError as e:
    #     print(e)
    #     error(f"Illegal number of arguments to command {cmd}.")
    # except Exception as e:
    #     print(e)
