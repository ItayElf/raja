import difflib
from typing import List
from rich.console import Console

from raja.actions import init, add, config, commit, rollback, status, login, push
from raja.utils import error


def raja_help():
    """Shows this message"""
    tuples = sorted(_commands.items(), key=lambda x: x[0])
    longest = max([len(c) for c, k in tuples])
    print("Commands:")
    console = Console()
    for c, f in tuples:
        console.print(f"\t[magenta]{c.ljust(longest, ' ')}[/magenta]\t[green]{f.__doc__}[/green]")


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
    "login": login.login,
    "push": push.push,
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
