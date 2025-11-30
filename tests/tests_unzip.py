import os.path

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from src.services.base import OSConsoleServiceBase


def test_unzip_for_nonexisted_archive(service: OSConsoleServiceBase, fs: FakeFilesystem):
    fs.create_file(os.path.join("data", "existing.zip"), contents="test")

    with pytest.raises(FileNotFoundError):
        service.unzip(
            os.path.join("data", "nonexisting.zip"),
        )


def test_unzip_for_invalid_archive_name(service: OSConsoleServiceBase, fs: FakeFilesystem):
    path = os.path.join("data", "archive.tar.gz")

    fs.create_file(path, contents="test")

    with pytest.raises(OSError):
        service.unzip(
            path,
        )
