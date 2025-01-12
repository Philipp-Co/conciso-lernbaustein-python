"""Token User which is used during authentication."""

#
# ---------------------------------------------------------------------------------------------------------------------
#
from logging import Logger, getLogger
from typing import Optional

from rest_framework_simplejwt.models import TokenUser
from rest_framework_simplejwt.tokens import Token

#
# ---------------------------------------------------------------------------------------------------------------------
#


class LabyrinthTokenUser(TokenUser):  # type: ignore[misc]
    def __init__(self, token: Token, logger: Optional[Logger] = None):
        super().__init__(token)
        self.__logger: Logger = logger if logger is not None else getLogger(self.__class__.__name__)
        pass

    def user_name(self) -> str:
        return self.token.get("preferred_username", "default")  # type: ignore[no-any-return]

    def is_allowed_to_solve(self) -> bool:
        try:
            realm_access = self.token.get("realm_access", None)
            if realm_access is not None:
                roles = realm_access["roles"]
                return "darf_labyrinth_loesen" in roles
            return False
        except Exception as e:
            self.__logger.exception(e)
            return False

    def is_allowed_to_load_new(self) -> bool:
        try:
            realm_access = self.token.get("realm_access", None)
            if realm_access is not None:
                roles = realm_access["roles"]
                return "darf_labyrinth_laden" in roles
            return False
        except Exception as e:
            self.__logger.exception(e)
            return False

    pass


#
# ---------------------------------------------------------------------------------------------------------------------
#
