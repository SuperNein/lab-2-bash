import os.path

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from src.services.base import OSConsoleServiceBase


def test_cp_for_nonexisted_file(service: OSConsoleServiceBase, fs: FakeFilesystem):
    fs.create_dir("data")
    fs.create_file(os.path.join("data", "existing.txt"), contents="test")

    with pytest.raises(FileNotFoundError):
        service.cp(
            os.path.join("data", "nonexisting.txt"),
            os.path.join("data", "existing.txt"),
            r_option=False,
        )


def test_cp_for_nonexisting_target_folder(service: OSConsoleServiceBase, fs: FakeFilesystem):
    fs.create_dir("data")
    fs.create_file(os.path.join("data", "existing.txt"), contents="test")

    with pytest.raises(FileNotFoundError):
        service.cp(
            os.path.join("data", "existing.txt"),
            os.path.join("nonexisting_folder", "nonexisting.txt"),
            r_option=False,
        )


def test_cp_for_nonexisted_source_folder(service: OSConsoleServiceBase, fs: FakeFilesystem):
    fs.create_dir(os.path.join("data", "existing_dir"))

    with pytest.raises(FileNotFoundError):
        service.cp(
            os.path.join("data", "nonexisting_dir"),
            os.path.join("data", "existing_dir"),
            r_option=True,
        )


def test_cp_for_folder_wo_recursive(service: OSConsoleServiceBase, fs: FakeFilesystem):
    fs.create_dir(os.path.join("data", "existing_dir"))

    with pytest.raises(IsADirectoryError):
        service.cp(
            os.path.join("data", "existing_dir"),
            os.path.join("data", "dir"),
            r_option=False,
        )


def test_recursive_cp_to_non_folder(service: OSConsoleServiceBase, fs: FakeFilesystem):
    dir_path = os.path.join("data", "existing_dir")
    file_path = os.path.join("data", "existing.txt")

    fs.create_dir(dir_path)
    fs.create_file(file_path, contents="test")

    with pytest.raises(IsADirectoryError):
        service.cp(
            dir_path,
            file_path,
            r_option=False,
        )


def test_cp(service: OSConsoleServiceBase, fs: FakeFilesystem):
    fs.create_dir("data")
    content = "test"

    path = os.path.join("data", "existing.txt")
    fs.create_file(path, contents=content)

    cp_path = os.path.join("data", "copy.txt")

    service.cp(
        path,
        cp_path,
        r_option=False,
    )

    with open(cp_path) as f:
        assert f.readline() == content
