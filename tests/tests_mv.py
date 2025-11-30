import os.path

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from src.services.base import OSConsoleServiceBase


def test_mv_for_nonexisted_file(service: OSConsoleServiceBase, fs: FakeFilesystem):
    dir_path = os.path.join("data", "dir")
    file_path = os.path.join("data", "existing.txt")

    fs.create_dir(dir_path)
    fs.create_file(file_path, contents="test")

    with pytest.raises(FileNotFoundError):
        service.mv(
            os.path.join("data", "nonexisting.txt"),
            dir_path,
        )


def test_mv_folder_to_non_folder(service: OSConsoleServiceBase, fs: FakeFilesystem):
    dir_path = os.path.join("data", "dir")
    file_path = os.path.join("data", "existing.txt")

    fs.create_dir(dir_path)
    fs.create_file(file_path, contents="test")

    with pytest.raises(NotADirectoryError):
        service.mv(
            dir_path,
            file_path,
        )
