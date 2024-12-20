from typing import List

from typing_extensions import Self


class Result:
    def __init__(self):
        self.__exit_reached: bool = False
        self.__gueltig: bool = True
        self.__beschreibungen: List[str] = []
        pass

    def add(self, text: str) -> Self:
        self.__beschreibungen.append(text)
        return self

    def valid(self, flag: bool) -> Self:
        self.__gueltig = flag
        return self

    def exit_reached(self, flag: bool) -> Self:
        self.__exit_reached = flag
        return self

    pass
