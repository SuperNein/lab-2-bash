import logging
from pathlib import Path

from src.services.args_filter import options_filter, args_filter
from src.services.path_funcs import path_stat, paths_to_abs
from src.states import current_dir as cwd


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
        try:
            path = paths_to_abs(args)[0]
        except Exception as e:
            self._logger.error(e, exc_info=True)
            raise e
        
        if not path.exists():
            self._logger.error(f'Folder not found: {path!r}')
            raise FileNotFoundError(f'{cmd}: cannot access {path!r}: No such file or directory')
        
        if not path.is_dir():
            self._logger.error(f'{path!r} is not a directory')
            raise NotADirectoryError(f'{cmd}: cannot access {path!r}: Not a directory')

        self._logger.info(f'Listing {path!r}')

        dirlist = []
        for entry in path.iterdir():
            entry_info = ''

            if '-l' in options:
                stat = path_stat(entry)
                entry_info = f'{stat['mode']} {stat['mtime']} {stat['size']:>15} {stat['name']}'
            else:
                entry_info = entry.name

            dirlist.append(entry_info)

        return dirlist
