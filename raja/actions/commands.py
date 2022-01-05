from typing import List

from raja.actions import init

_commands = {
    "init": init.init,
    "destroy": init.destroy
}


def handle_command(cmd: str, parans: List[str]) -> None:
    """Calls a command based on its name and the given parameters"""
    if cmd not in _commands:
        print(f"Illegal command: {cmd}.")
        return
    try:
        _commands[cmd](*parans)
    except TypeError:
        print(f"Illegal number of arguments to command {cmd}")
    # except Exception as e:
    #     print(e)
