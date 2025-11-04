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
        path = paths_to_abs(args)[0]
        
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


    @options_filter(available_options=[])
    @args_filter(args_num=[0, 1])
    def cd(self, cmd: str, options: list, args: list):
        path = paths_to_abs(args)[0]

        if not path.exists():
            self._logger.error(f'Folder not found: {path!r}')
            raise FileNotFoundError(f'{cmd}: cannot access {path!r}: No such file or directory')

        if not path.is_dir():
            self._logger.error(f'{path!r} is not a directory')
            raise NotADirectoryError(f'{cmd}: cannot access {path!r}: Not a directory')

        self._logger.info(f'Transition to {path!r}')

        cwd.current_dir = path


    @options_filter(available_options=[])
    @args_filter(args_num=[0, 1])
    def cat(self, cmd: str, options: list, args: list):
        path = paths_to_abs(args)[0]

        if not path.exists():
            self._logger.error(f'File not found: {path!r}')
            raise FileNotFoundError(f'{cmd}: cannot access {path!r}: No such file or directory')

        if path.is_dir():
            self._logger.error(f'{path!r} is not a directory')
            raise IsADirectoryError(f'{cmd}: cannot access {path!r}: Is a directory')

        self._logger.info(f'Read file {path!r}')

        return path.read_text(encoding="utf-8").splitlines()
