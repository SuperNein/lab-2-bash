from os import PathLike
from pathlib import Path
from stat import filemode
from datetime import datetime


def path_stat(path: Path) -> dict[str, str]:
    """
    Return stat of directory or file from path
    :param path:    path to file of directory
    :return:    dict = {
        'name': str,
        'mode': str,
        'mtime': str,
        'size': str
    }
    """
    stat = path.stat()
    path_info = {
        'name': path.name,
        'mode': filemode(stat.st_mode),
        'mtime': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
        'size': stat.st_size,
    }

    return path_info
