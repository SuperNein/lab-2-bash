import os.path

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from src.services.base import OSConsoleServiceBase


def test_zip_for_nonexisted_folder(service: OSConsoleServiceBase, fs: FakeFilesystem):
    fs.create_dir(os.path.join("data", "existing_dir"))

    with pytest.raises(FileNotFoundError):
        service.zip(
            os.path.join("data", "nonexisting_dir"),
            "archive.zip.gz",
        )


def test_zip_for_invalid_archive_name(service: OSConsoleServiceBase, fs: FakeFilesystem):
    dir_path = os.path.join("data", "dir")

    fs.create_dir(dir_path)

    with pytest.raises(OSError):
        service.zip(
            dir_path,
            "archive.tar.gz",
        )
