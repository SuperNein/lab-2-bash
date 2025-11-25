from src.common.config import LOGGING_CONFIG

import logging
import sys
import os
from pathlib import Path
from shlex import split as shlex_split

import typer
from typer import Typer, Context

from src.dependencies.container import Container
from src.services.console import OSConsoleService

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
        _container = Container(console_service=OSConsoleService(logger=_logger))


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
    typer.echo(">>> Start the interactive session")

    while (user_input:=typer.prompt(f"{os.getcwd()}", prompt_suffix="> ")) != "exit":
        command = shlex_split(user_input)
        try:
            app(command)
        except SystemExit:
            pass


@app.command("exit")
def exit_cmd(
        ctr: Context,
) -> None:
    """
    Exit interactive session.
    :param ctr: typer context object for imitating di container
    :return:
    """
    pass


@app.command()
def ls(
    ctx: Context,
    path: Path = typer.Argument(
        "./", exists=False, readable=False, help="Path for listing",
    ),
    l_option: bool = typer.Option(
        False, "-l", help="Use long listing format"
    ),
) -> None:
    """
    List all files in a directory.
    :param ctx:   typer context object for imitating di container
    :param path:  path to directory to list
    :param l_option:  use long listing format
    :return:
    """
    try:
        container: Container = get_container()
        content = container.console_service.ls(path, l_option)
        sys.stdout.writelines(content)
    except OSError as e:
        typer.echo(f"{ctx.command.name}: {e}")


@app.command()
def cd(
    ctx: Context,
    path: Path = typer.Argument(
        ..., exists=False, readable=False, help="Directory to make current"
    ),
) -> None:
    """
    Make a directory current.
    :param ctx: typer context object for imitating di container
    :param path: Directory to make current
    :return:
    """
    try:
        container: Container = get_container()
        container.console_service.cd(path)
    except OSError as e:
        typer.echo(f"{ctx.command.name}: {e}")


@app.command()
def cat(
    ctx: Context,
    path: Path = typer.Argument(
        ..., exists=False, readable=False, help="File to print"
    ),
) -> None:
    """
    Cat a file.
    :param ctx: typer context object for imitating di container
    :param path: Filename to cat
    :return:
    """
    try:
        container: Container = get_container()
        data = container.console_service.cat(
            path,
        )
        sys.stdout.write(data)
    except OSError as e:
        typer.echo(f"{ctx.command.name}: {e}")


@app.command()
def cp(
    ctx: Context,
    path_from: Path = typer.Argument(
        ..., exists=False, readable=False, help="Path to copy"
    ),
    path_to: Path = typer.Argument(
        ..., exists=False, readable=False, help="Path where copying"
    ),
    r_option: bool = typer.Option(
        False, "-r", help="Copy directories recursively"
    ),
) -> None:
    """
    Copy file.
    :param ctx: typer context object for imitating di container
    :param path_from: path to copy
    :param path_to: path where copying
    :param r_option:  recursive mode
    :return:
    """
    try:
        container: Container = get_container()
        container.console_service.cp(path_from, path_to, r_option)
    except OSError as e:
        typer.echo(f"{ctx.command.name}: {e}")


@app.command()
def mv(
    ctx: Context,
    path_from: Path = typer.Argument(
        ..., exists=False, readable=False, help="Path for moving"
    ),
    path_to: Path = typer.Argument(
        ..., exists=False, readable=False, help="Path where moving"
    ),
) -> None:
    """
    Move file or directory.
    :param ctx: typer context object for imitating di container
    :param path_from: path for moving
    :param path_to: path where moving
    :return:
    """
    try:
        container: Container = get_container()
        container.console_service.mv(path_from, path_to)
    except OSError as e:
        typer.echo(f"{ctx.command.name}: {e}")


@app.command()
def rm(
    ctx: Context,
    path: Path = typer.Argument(
        ..., exists=False, readable=False, help="Path for removing"
    ),
    r_option: bool = typer.Option(
        False, "-r", help="Copy directories recursively"
    ),
) -> None:
    """
    Remove file or directory.
    :param ctx: typer context object for imitating di container
    :param path: path for removing
    :param r_option:  recursive mode
    :return:
    """
    try:
        container: Container = get_container()
        container.console_service.rm(path, r_option)
    except OSError as e:
        typer.echo(f"{ctx.command.name}: {e}")


@app.command("zip")
def zip_cmd(
    ctx: Context,
    folder: Path = typer.Argument(
        ..., exists=False, readable=False, help="Folder for archiving to .zip"
    ),
    archive: str = typer.Argument(
        ..., help="Archive.zip name"
    ),
) -> None:
    """
    Archive folder to .zip.
    :param ctx:   typer context object for imitating di container
    :param folder:   path of folder to archive
    :param archive:   archive name with '.zip' type
    :return:
    """
    try:
        container: Container = get_container()
        container.console_service.zip(folder, archive)
    except OSError as e:
        typer.echo(f"{ctx.command.name}: {e}")


@app.command()
def unzip(
    ctx: Context,
    archive: Path = typer.Argument(
        ..., exists=False, readable=False, help="Archive.zip to unzip"
    ),
) -> None:
    """
    Unzip zipfile
    :param ctx:   typer context object for imitating di container
    :param archive:   archive.zip to unzip
    :return:
    """
    try:
        container: Container = get_container()
        container.console_service.unzip(archive)
    except OSError as e:
        typer.echo(f"{ctx.command.name}: {e}")


@app.command()
def tar(
    ctx: Context,
    folder: Path = typer.Argument(
        ..., exists=False, readable=False, help="Folder for archiving to .tar.gz"
    ),
    archive: str = typer.Argument(
        ..., help="Archive.tar.gz name"
    ),
) -> None:
    """
    Archive folder to .tar.gz.
    :param ctx:   typer context object for imitating di container
    :param folder:   path of folder to archive
    :param archive:   archive name with '.tar.gz' type
    :return:
    """
    try:
        container: Container = get_container()
        container.console_service.tar(folder, archive)
    except OSError as e:
        typer.echo(f"{ctx.command.name}: {e}")


if __name__ == "__main__":
    app()
