"""This is an interface definition for Clients."""
# ---------------------------------------------------------------------------------------------------------------------
from abc import ABC, abstractmethod
from typing import Dict
from logging import Logger
from typing_extensions import Self
# ---------------------------------------------------------------------------------------------------------------------

class IClient(ABC):
    
    def __init__(self):
        self.__logger: Optional[Logger] = None
        pass

    def set_logger(self, logger: Logger) -> Self:
        self.__logger = logger
        return self

    def logger(self) -> Logger:
        return self.__logger

    @abstractmethod
    def run(self, args: Dict[str, str]) -> int:
        """Run the clientcode.
        
        If this function returns the program exits and returns the status code to the user.
        """
        pass

    pass
# ---------------------------------------------------------------------------------------------------------------------
