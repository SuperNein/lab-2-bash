import logging
import os
import shutil
from logging import Logger
from os import PathLike
from pathlib import Path
from zipfile import ZipFile

from src.services.base import OSConsoleServiceBase
from src.services.path_funcs import path_stat
from src.services.typer_echo import typer_confirm
from src.common.constants import TRASH_DIR


class OSConsoleService(OSConsoleServiceBase):
    def __init__(self, logger: Logger):
        self._logger = logger


    def ls(self, path: PathLike[str] | str, l_option: bool) -> list[str]:
        path = Path(path).expanduser().resolve()

        if not path.exists():
            self._logger.error(f"Folder not found: {path}")
            raise FileNotFoundError(f'Cannot access {path}: No such file or directory')

        if not path.is_dir():
            self._logger.error(f"You entered {path} is not a directory")
            raise NotADirectoryError(f"Cannot access {path}: Not a directory")

        self._logger.info(f"Listing {path}")

        dirlist = []
        for entry in path.iterdir():
            if l_option:
                stat = path_stat(entry)
                entry_info = f'{stat['mode']} {stat['mtime']} {stat['size']:>15} {stat['name']}'
            else:
                entry_info = entry.name

            dirlist.append(entry_info + '\n')

        return dirlist


    def cd(self, path: PathLike[str] | str) -> None:
        path = Path(path).expanduser().resolve()

        if not path.exists():
            self._logger.error(f"Folder not found: {path}")
            raise FileNotFoundError(f'Cannot access {path}: No such file or directory')

        if not path.is_dir():
            self._logger.error(f"You entered {path} is not a directory")
            raise NotADirectoryError(f"Cannot access {path}: Not a directory")

        self._logger.info(f"Make current {path}")

        os.chdir(path)


    def cat(
        self,
        path: PathLike[str] | str,
    ) -> str:

        path = Path(path).expanduser().resolve()

        if not path.exists(follow_symlinks=True):
            self._logger.error(f"File not found: {path}")
            raise FileNotFoundError(f'Cannot access {path}: No such file or directory')

        if path.is_dir(follow_symlinks=True):
            self._logger.error(f"You entered {path} is not a file")
            raise IsADirectoryError(f"Cannot access {path!r}: Is a directory")

        self._logger.info(f"Reading file {path}")

        return path.read_text(encoding="utf-8")


    def cp(
        self,
        path_from: PathLike[str] | str,
        path_to: PathLike[str] | str,
        r_option: bool,
    ) -> None:

        path_from = Path(path_from).expanduser().resolve()
        path_to = Path(path_to).expanduser().resolve()

        if not path_from.exists(follow_symlinks=True):
            self._logger.error(f"File not found: {path_from}")
            raise FileNotFoundError(f'Cannot access {path_from}: No such file or directory')

        if path_from.is_file():
            self._logger.info(f"Copying {path_from}")
            shutil.copy2(str(path_from), str(path_to))

        elif path_from.is_dir():
            if not r_option:
                self._logger.error(f"Copying dict as a file: {path_from}")
                raise IsADirectoryError(f"-r not specified; omitting directory {path_from}")

            if not path_to.is_dir():
                self._logger.error(f"Copying dict to file: {path_from}")
                raise NotADirectoryError(f"cannot overwrite non-directory {path_to} with directory {path_from}")

            self._logger.info(f"Copying {path_from}")
            shutil.copytree(path_from, path_to, dirs_exist_ok=True)


    def mv(
        self,
        path_from: PathLike[str] | str,
        path_to: PathLike[str] | str,
    ) -> None:

        path_from = Path(path_from).expanduser().resolve()
        path_to = Path(path_to).expanduser().resolve()

        if not path_from.exists(follow_symlinks=True):
            self._logger.error(f"File not found: {path_from}")
            raise FileNotFoundError(f'Cannot access {path_from}: No such file or directory')

        if path_from.is_dir() and path_to.exists() and path_to.is_file():
            self._logger.error(f"Copying dict to file: {path_from}")
            raise NotADirectoryError(f"cannot overwrite non-directory {path_to} with directory {path_from}")

        try:
            shutil.move(path_from, path_to)
            self._logger.info(f"Moving {path_from} to {path_to}")
        except PermissionError:
            self._logger.error(f"No execute permission for target.")
            raise PermissionError(f"no execute permission for target.")


    def rm(
            self,
            path: PathLike[str] | str,
            r_option: bool,
    ) -> None:
        path = Path(path).expanduser().resolve()

        if not path.exists(follow_symlinks=True):
            self._logger.error(f"File not found: {path}")
            raise FileNotFoundError(f'Cannot access {path}: No such file or directory')

        home_dir = Path.home()
        if path in (home_dir, home_dir.root, home_dir.parent):
            self._logger.error(f"No execute permission for target {path}")
            raise PermissionError(f'no execute permission for target {path}')

        if path.is_dir():
            if not r_option:
                self._logger.error(f"Removing dict as a file: {path}")
                raise IsADirectoryError(f"-r not specified; omitting directory {path}")

            if typer_confirm():
                shutil.move(path, TRASH_DIR)

        else:
            shutil.move(path, TRASH_DIR)

        self._logger.info(f"Removing {path}")


    def zip(
        self,
        folder: PathLike[str] | str,
        archive: str,
    ) -> None:

        folder = Path(folder).expanduser().resolve()

        if not folder.exists():
            self._logger.error(f"File not found: {folder}")
            raise FileNotFoundError(f'Cannot access {folder}: No such file or directory')

        if not archive.endswith(".zip"):
            self._logger.error(f"Archive {archive} must be named with .zip")
            raise OSError(f"Cannot make {archive}: Must be named with .zip")

        self._logger.info(f"Archiving {folder} to zip")

        with ZipFile(archive, "w") as zipfile:
            for item in folder.rglob("*"):
                zipfile.write(item, arcname=item.relative_to(folder))


    def unzip(
        self,
        archive: PathLike[str] | str,
    ) -> None:

        archive = Path(archive).expanduser().resolve()

        if not archive.exists():
            self._logger.error(f"File not found: {archive}")
            raise FileNotFoundError(f'Cannot access {archive}: No such file or directory')

        if not archive.name.endswith(".zip"):
            self._logger.error(f"Archive {archive} must be named with .zip")
            raise OSError(f"Cannot unzip {archive}: No zip file")

        self._logger.info(f"Unzipping {archive}")

        with ZipFile(archive, "r") as zipfile:
            zipfile.extractall(archive.parent)
