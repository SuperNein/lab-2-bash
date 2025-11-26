from logging import Logger

import pytest
from pytest_mock import MockerFixture

from src.services.console import OSConsoleService


@pytest.fixture
def logger(mocker: MockerFixture) -> Logger:
    return mocker.Mock()


@pytest.fixture
def service(logger: Logger):
    return OSConsoleService(logger)
