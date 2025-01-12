"""A Service that checks for authentication."""
#
# ---------------------------------------------------------------------------------------------------------------------
#
from logging import Logger

from labyrinth.models.adventurer import Adventurer
from labyrinth.models.client import Client

#
# ---------------------------------------------------------------------------------------------------------------------
#


class AuthenticationService:
    def __init__(self, username: str, logger: Logger):
        self.__username: str = username
        self.__logger: Logger = logger
        pass

    def username(self) -> str:
        return self.__username

    def is_allowed_to_move_adventurer(self, adventurer: str) -> bool:
        try:
            self.__logger.info(f"Try to find client for user {self.username()}")
            client = Client.objects.get(user_name=self.username())
            adventurer_list = Adventurer.objects.filter(client=client)
            self.__logger.info(f"Adventurer for client {client}: {adventurer_list}")
            for adventurer_object in adventurer_list:
                if adventurer_object.name == adventurer:
                    return True
        except Exception as e:
            self.__logger.exception(e)
        return False

    pass


#
# ---------------------------------------------------------------------------------------------------------------------
#
