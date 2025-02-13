from abc import ABC, abstractmethod
from dataclasses import dataclass


class IAuthentication(ABC):
    @abstractmethod
    def get_bearer_token(self) -> str:
        pass

    pass
