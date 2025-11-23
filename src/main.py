from src.common.config import LOGGING_CONFIG

import logging
import sys
import os
from pathlib import Path
from shlex import split as shlex_split

import typer
from typer import Typer, Context

from src.dependencies.container import Container
from src.services.console import ConsoleService

_logger = None
_container = None

app = Typer()


def get_container() -> Container:
    """
    Return global container object if initialized.
    :return: global container object
    """
    global _container
    if not isinstance(_container, Container):
        raise RuntimeError("DI container is not initialized")
    return _container


def init_container() -> None:
    """
    Initialize global logger and container object if not initialized.
    :return:   None
    """
    global _logger, _container
    if not isinstance(_container, Container):
        logging.config.dictConfig(LOGGING_CONFIG)
        _logger = logging.getLogger(__name__)
        _container = Container(console_service=ConsoleService(logger=_logger))


@app.callback()
def main(ctx: Context) -> None:
    """
    Initialize and push di container from global to typer context object.
    :param ctx:   typer context object for set di container
    :return:   None
    """
    init_container()
    ctx.obj = _container


@app.command(hidden=True)
def run(ctx: Context) -> None:
    """
    Run interactive CLI.
    :param ctx:   typer context object for imitating di container
    :return:   None
    """
    typer.echo("Welcome to the interactive Typer session!")

    while (user_input:=typer.prompt(f"{os.getcwd()}", prompt_suffix="> ")) != "exit":
        command = shlex_split(user_input)
        try:
            app(command)
        except SystemExit:
            pass


@app.command()
def ls(
    ctx: Context,
    path: Path = typer.Argument(
        os.getcwd(), exists=False, readable=False, help="Path for listing"
    ),
) -> None:
    """
    List all files in a directory.
    :param ctx:   typer context object for imitating di container
    :param path:  path to directory to list
    :return: content of directory
    """
    try:
        container: Container = get_container()
        content = container.console_service.ls(path)
        sys.stdout.writelines(content)
    except OSError as e:
        typer.echo(e)


@app.command()
def cat(
    ctx: Context,
    filename: Path = typer.Argument(
        ..., exists=False, readable=False, help="File to print"
    ),
) -> None:
    """
    Cat a file.
    :param ctx: typer context object for imitating di container
    :param filename: Filename to cat
    :return:
    """
    try:
        container: Container = get_container()
        data = container.console_service.cat(
            filename,
        )
        if isinstance(data, bytes):
            sys.stdout.buffer.write(data)
        else:
            sys.stdout.write(data)
    except OSError as e:
        typer.echo(e)


if __name__ == "__main__":
    app()
