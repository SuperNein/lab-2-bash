import logging
from os import PathLike
from pathlib import Path


class Console:
    def __init__(self, logger: logging.Logger):
        self._logger = logger

    def exit(self, cmd: str, options: list, args: list) -> None:
        self._logger.info(f'Interrupted by command: {cmd}')
        raise KeyboardInterrupt

    def ls(self, cmd: str, options: list, args: list):
        pass
