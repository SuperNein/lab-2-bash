from abc import ABC, abstractmethod
from os import PathLike
from typing import Literal


class OSConsoleServiceBase(ABC):
    @abstractmethod
    def ls(self, path: PathLike[str] | str) -> list[str]: ...

    @abstractmethod
    def cat(
        self,
        filename: PathLike | str,
    ) -> str | bytes: ...
