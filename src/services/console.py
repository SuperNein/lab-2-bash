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

    @options_filter(available_options=['-l'])
    @args_filter(args_num=[0, 1])
    def ls(self, cmd: str, options: list, args: list) -> list[str]:
        if args:
            path = Path(args[0])
            if not path.is_absolute():
                path = (current_dir / path).resolve()
        else:
            path = current_dir
        
        if not path.exists():
            self._logger.error(f'Folder not found: {path!r}')
            raise FileNotFoundError(f'{cmd}: cannot access {path!r}: No such file or directory')
        
        if not path.is_dir():
            self._logger.error(f'{path!r} is not a directory')
            raise NotADirectoryError(f'{cmd}: cannot access {path!r}: Not a directory')

        self._logger.info(f'Listing {path!r}')
        return [entry.name for entry in path.iterdir()]
