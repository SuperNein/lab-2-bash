from abc import ABC, abstractmethod
from os import PathLike
from typing import Literal


class OSConsoleServiceBase(ABC):
    @abstractmethod
    def ls(
            self,
            path: PathLike[str] | str,
            l_option: bool,
    ) -> list[str]: ...

    @abstractmethod
    def cd(self, path: PathLike[str] | str) -> None: ...

    @abstractmethod
    def cat(self, filename: PathLike | str) -> str: ...

    @abstractmethod
    def cp(
            self,
            path_from: PathLike[str] | str,
            path_to: PathLike[str] | str,
            r_option: bool,
    ) -> None: ...

    @abstractmethod
    def mv(
            self,
            path_from: PathLike[str] | str,
            path_to: PathLike[str] | str,
    ) -> None: ...