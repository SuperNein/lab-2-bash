import logging
from os import PathLike
from pathlib import Path

from src.services.args_filter import options_filter


class Console:
    def __init__(self, logger: logging.Logger):
        self._logger = logger

    @options_filter()
    def exit(self, cmd: str, options: list, args: list) -> None:
        self._logger.info(f'Interrupted by command: {cmd}')
        raise KeyboardInterrupt

    @options_filter(['-l'])
    def ls(self, cmd: str, options: list, args: list):
        pass
