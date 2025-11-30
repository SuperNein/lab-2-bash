import os.path

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from src.services.base import OSConsoleServiceBase


def test_untar_for_nonexisted_archive(service: OSConsoleServiceBase, fs: FakeFilesystem):
    fs.create_file(os.path.join("data", "existing.tar.gz"), contents="test")

    with pytest.raises(FileNotFoundError):
        service.untar(
            os.path.join("data", "nonexisting.tar.gz"),
        )


def test_untar_for_invalid_archive_name(service: OSConsoleServiceBase, fs: FakeFilesystem):
    path = os.path.join("data", "archive.zip")

    fs.create_file(path, contents="test")

    with pytest.raises(OSError):
        service.untar(
            path,
        )
