import logging
import os
from logging import Logger
from os import PathLike
from pathlib import Path
from typing import Literal

from src.services.base import OSConsoleServiceBase
from src.services.path_funcs import path_stat


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
