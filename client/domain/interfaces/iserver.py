from abc import ABC, abstractmethod
from dataclasses import dataclass

from typing_extensions import Self


@dataclass
class Location:
    north: str
    east: str
    south: str
    west: str
    current: str
    pass


@dataclass
class Result:
    return_value: bool
    description: str
    pass


class IServer(ABC):
    @abstractmethod
    def where_am_i(self) -> Location:
        pass

    @abstractmethod
    def move(self, direction: str) -> bool:
        pass

    pass
