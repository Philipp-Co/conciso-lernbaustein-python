# ---------------------------------------------------------------------------------------------------------------------
from dataclasses import dataclass
from http import HTTPStatus
from json import loads
from logging import Logger, getLogger
from typing import Any

from domain.authentication.oidc_url_form_encoded import (
    IamProviderInfo,
    OidcUrlFormEncodedAuthentication,
)
from domain.interfaces.iauthentication import IAuthentication
from domain.interfaces.iserver import IServer, Location
from requests import Response, get, post
from typing_extensions import Self

# ---------------------------------------------------------------------------------------------------------------------


class DefaultServerAuthenticationHandler(IAuthentication):
    def get_bearer_token(self, parameter: IamProviderInfo) -> str:
        raise NotImplementedError("Authentication not Implemented!")

    pass


# ---------------------------------------------------------------------------------------------------------------------


class Server(IServer):
    def __init__(self, url: str, name: str, labyriths_name: str, logger: Logger):
        self.__authentication_handler: IAuthentication = DefaultServerAuthenticationHandler()
        self.__logger: Logger = logger
        self.__url: str = url
        self.__name: str = name
        self.__labyrinths_name: str = labyriths_name
        pass

    def set_authentication_handler(self, handler: IAuthentication) -> Self:
        self.__authentication_handler = handler
        return self

    def where_am_i(self) -> Location:
        try:
            response: Response = get(
                f"{self.__url}navigate/{self.__name}/",
                headers={
                    "Authorization": f"Bearer {self.__authentication_handler.get_bearer_token()}",
                },
            )
            content: Any = loads(response.content.decode("utf-8"))
            if response.status_code == HTTPStatus.OK:
                self.__logger.info(f'return_value: {content["return_value"]}, {content["description"]}')
                if content["return_value"]:
                    return Location(
                        north=content["north_tile"],
                        east=content["east_tile"],
                        south=content["south_tile"],
                        west=content["west_tile"],
                        current=content["current_tile"],
                    )
            else:
                self.__logger.error(f'HTTP Status: {response.status_code}, {content["description"]}')
        except Exception as e:
            self.__logger.exception(e)
        raise AssertionError("Call to API was not Successfull.")

    def move(self, direction: str) -> bool:
        self.__logger.info(f"Request a move to: {direction}.")
        try:
            response: Response = post(
                f"{self.__url}navigate/{self.__name}/",
                json={
                    "direction": direction,
                },
                headers={
                    "Authorization": f"Bearer {self.__authentication_handler.get_bearer_token()}",
                },
            )
            content: Any = loads(response.content.decode("utf-8"))
            if response.status_code == HTTPStatus.OK:
                self.__logger.info(
                    f'return_value: {content["return_value"]}, solved: {content["solved"]}, {content["description"]}'
                )
                return content["solved"]
            else:
                self.__logger.error(f'HTTP Status: {response.status_code}, {content["description"]}')
        except Exception as e:
            self.__logger.exception(e)
        raise AssertionError("API call was not successfull.")

    pass


# ---------------------------------------------------------------------------------------------------------------------


class ServerFactory:
    def __init__(self, logger: Logger):
        self.__logger: Logger = logger
        pass

    def create(self, backend_url: str, adventurer: str, labyrinths_name: str, iam_info: IamProviderInfo) -> IServer:
        return Server(
            url=backend_url,
            name=adventurer,
            labyriths_name=labyrinths_name,
            logger=self.__logger.getChild(Server.__name__),
        ).set_authentication_handler(
            OidcUrlFormEncodedAuthentication(
                iam_info=iam_info,
                logger=self.__logger.getChild(OidcUrlFormEncodedAuthentication.__name__),
            )
        )

    pass


# ---------------------------------------------------------------------------------------------------------------------
