import os.path

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from src.services.base import OSConsoleServiceBase


def test_cat_for_nonexisted_file(service: OSConsoleServiceBase, fs: FakeFilesystem):
    # Arrange
    fs.create_dir("data")
    fs.create_file(os.path.join("data", "existing.txt"), contents="test")

    # Act
    with pytest.raises(FileNotFoundError):
        service.cat(os.path.join("data", "nonexisting.txt"))


def test_cat_for_folder(service: OSConsoleServiceBase, fs: FakeFilesystem):
    fs.create_dir("data")
    fs.create_file(os.path.join("data", "existing.txt"), contents="test")

    with pytest.raises(IsADirectoryError):
        service.cat("data")


def test_cat_file_with_text(service: OSConsoleServiceBase, fs: FakeFilesystem):
    fs.create_dir("data")
    content = "test"
    path = os.path.join("data", "existing.txt")
    fs.create_file(path, contents=content)

    result = service.cat(path)

    assert result == content
