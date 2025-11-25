from typer import confirm, echo

from src.common.constants import HISTORY_PATH


def typer_confirm():
    if confirm("You are trying to delete a directory. Continue?"):
        return True

    else:
        echo("Cancelling command")
        return False

def write_history(cmdline: str) -> None:
    """
    Write the history of the command to file with src.common.constants.HISTORY_PATH
    :param cmdline:   commandline to write to history file
    :return:
    """
    if not HISTORY_PATH.exists():
        HISTORY_PATH.touch()
    with open(HISTORY_PATH, "a", encoding='utf-8') as f:
        f.write(f"{cmdline}\n")
