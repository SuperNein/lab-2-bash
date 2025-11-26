import os.path

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from src.services.base import OSConsoleServiceBase

def test_cd_for_nonexisted_folder(service: OSConsoleServiceBase, fs: FakeFilesystem):
    fs.create_dir(os.path.join("data", "existing_dir"))

    with pytest.raises(FileNotFoundError):
        service.cd(os.path.join("data", "nonexisting_dir"))


def test_cd_for_no_folder(service: OSConsoleServiceBase, fs: FakeFilesystem):
    path = os.path.join("data", "existing.txt")

    fs.create_file(path)

    with pytest.raises(NotADirectoryError):
        service.cd(os.path.join("data", "existing.txt"))


def test_cd_for_existed_folder(service: OSConsoleServiceBase, fs: FakeFilesystem):
    path = os.path.join("data", "existing_dir")
    path = os.path.abspath(path)

    fs.create_dir(path)
    service.cd(path)

    assert path == fs.cwd
