import os.path

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from src.services.base import OSConsoleServiceBase

def test_ls_for_nonexisted_folder(service: OSConsoleServiceBase, fs: FakeFilesystem):
    path = os.path.join("data", "dir")

    fs.create_dir(path)
    fs.create_file(os.path.join(path, "f1.txt"))
    fs.create_file(os.path.join(path, "f2.txt"))

    with pytest.raises(FileNotFoundError):
        service.ls(os.path.join("data", "nonexisting_dir"), False)


def test_ls_for_no_folder(service: OSConsoleServiceBase, fs: FakeFilesystem):
    path = os.path.join("data", "dir")

    fs.create_dir(path)
    fs.create_file(os.path.join(path, "f1.txt"))
    fs.create_file(os.path.join(path, "f2.txt"))

    with pytest.raises(NotADirectoryError):
        service.ls(os.path.join(path, "f1.txt"), False)
