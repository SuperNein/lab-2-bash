import logging
from os import PathLike
from pathlib import Path


class Console:
    def __init__(self, logger: logging.Logger):
        self._logger = logger

    def ls(self, path: PathLike[str] | str):
        path = Path(path)
        return
