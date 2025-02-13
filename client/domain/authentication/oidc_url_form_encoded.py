# ---------------------------------------------------------------------------------------------------------------------
from dataclasses import dataclass
from json import loads
from logging import Logger

from domain.interfaces.iauthentication import IAuthentication
from requests import Response, post

# ---------------------------------------------------------------------------------------------------------------------


@dataclass
class IamProviderInfo:
    url: str
    username: str
    password: str
    pass


# ---------------------------------------------------------------------------------------------------------------------


class OidcUrlFormEncodedAuthentication(IAuthentication):
    def __init__(self, iam_info: IamProviderInfo, logger: Logger):
        super().__init__()
        self.__info: IamProviderInfo = iam_info
        self.__logger: Logger = logger
        pass

    def get_bearer_token(self) -> str:
        response: Response = post(
            self.__info.url,
            {
                "username": self.__info.username,
                "password": self.__info.password,
                "grant_type": "password",
                "client_id": "clp-client",
            },
            {
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        self.__logger.info(f'Response was: {response.content.decode("utf-8")}')
        return loads(response.content.decode("utf-8"))["access_token"]

    pass


# ---------------------------------------------------------------------------------------------------------------------
