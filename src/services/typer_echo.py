from typer import confirm, echo

def typer_confirm():
    if confirm("You are trying to delete a directory. Continue?"):
        return True

    else:
        echo("Cancelling command")
        return False
