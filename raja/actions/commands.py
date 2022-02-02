import difflib
from typing import List

from raja.actions import init, add, config, commit, rollback, status
from raja.utils import error


def raja_help():
    """Shows this message"""
    tuples = sorted(_commands.items(), key=lambda x: x[0])
    longest = max([len(c) for c, k in tuples])
    print("Commands:")
    for c, f in tuples:
        print(f"\t{c.ljust(longest, ' ')}\t{f.__doc__}")  # TODO: make colorful


_commands = {
    "init": init.init,
    "destroy": init.destroy,
    "reset": init.reset,
    "add": add.add,
    "remove": add.remove,
    "config": config.config,
    "commit": commit.commit,
    "rollback": rollback.rollback,
    "status": status.status,
    "help": raja_help,
}


def handle_command(cmd: str, params: List[str]) -> None:
    """Calls a command based on its name and the given parameters"""
    if cmd not in _commands:
        error(f"Illegal command: '{cmd}'")
        closest_matches_str = "\n\t".join(difflib.get_close_matches(cmd, _commands.keys()))
        if closest_matches_str:
            print(f"Similar commands: \n\t{closest_matches_str}")
        return
    # try:
    _commands[cmd](*params)
    # except TypeError as e:
    #     print(e)
    #     error(f"Illegal number of arguments to command {cmd}.")
    # except Exception as e:
    #     print(e)
