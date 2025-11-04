from pathlib import Path
from stat import filemode
from datetime import datetime

from src.states import current_dir as cwd


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


def paths_to_abs(paths_args: list[str]) -> list[Path]:
    """
    Convert string paths to absolute Path objects.
    If :paths_args: is empty list, return list with current directory
    :param paths_args:    list of str paths
    :return:    list of absolute Path objects
    """
    paths = []
    if paths_args:

        for path_str in paths_args:
            path = Path(path_str)
            if '~' in path_str:
                path = path.expanduser()

            if not path.is_absolute():
                path = (cwd.current_dir / path).resolve()
            paths.append(path)

    else:
        paths.append(cwd.current_dir)

    return paths
