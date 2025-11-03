import logging
from os import PathLike
from pathlib import Path

from src.services.args_filter import options_filter, args_filter
from src.states.current_dir import current_dir


class Console:
    def __init__(self, logger: logging.Logger):
        self._logger = logger

    @options_filter(available_options=[])
    @args_filter(args_num=[0])
    def exit(self, cmd: str, options: list, args: list) -> None:
        self._logger.info(f'Interrupted by command: {cmd}')
        raise KeyboardInterrupt

    @options_filter(['-l'])
    def ls(self, cmd: str, options: list, args: list):
        pass
