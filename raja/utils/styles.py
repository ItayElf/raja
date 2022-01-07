from rich.console import Console


def error(err: str):
    """Prints an error message"""
    c = Console()
    c.print(err, style="red bold")


def success(msg: str) -> None:
    """Prints a success message"""
    c = Console()
    c.print(msg, style="green bold")
