import os.path

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from src.services.base import OSConsoleServiceBase


def test_rm_for_nonexisted_file(service: OSConsoleServiceBase, fs: FakeFilesystem):
    dir_path = os.path.join("data", "dir")
    file_path = os.path.join("data", "existing.txt")

    fs.create_dir(dir_path)
    fs.create_file(file_path, contents="test")

    with pytest.raises(FileNotFoundError):
        service.rm(
            os.path.join("data", "nonexisting.txt"),
            r_option=False,
        )


def test_rm_for_folder_wo_recursive(service: OSConsoleServiceBase, fs: FakeFilesystem):
    dir_path = os.path.join("data", "dir")

    fs.create_dir(dir_path)

    with pytest.raises(IsADirectoryError):
        service.rm(
            dir_path,
            r_option=False,
        )
