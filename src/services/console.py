import logging
from logging import Logger
from os import PathLike
from pathlib import Path
from typing import Literal

from src.services.base import OSConsoleServiceBase


class OSConsoleService(OSConsoleServiceBase):
    def __init__(self, logger: Logger):
        self._logger = logger


    def ls(self, path: PathLike[str] | str) -> list[str]:
        path = Path(path)

        if not path.exists():
            self._logger.error(f"Folder not found: {path}")
            raise FileNotFoundError(path)

        if not path.is_dir():
            self._logger.error(f"You entered {path} is not a directory")
            raise NotADirectoryError(path)

        self._logger.info(f"Listing {path}")

        return [entry.name + "\n" for entry in path.iterdir()]

    def cat(
        self,
        filename: PathLike[str] | str,
    ) -> str:

        path = Path(filename)

        if not path.exists(follow_symlinks=True):
            self._logger.error(f"File not found: {filename}")
            raise FileNotFoundError(filename)

        if path.is_dir(follow_symlinks=True):
            self._logger.error(f"You entered {filename} is not a file")
            raise IsADirectoryError(f"You entered {filename} is not a file")

        self._logger.info(f"Reading file {filename}")

        return path.read_text(encoding="utf-8")
