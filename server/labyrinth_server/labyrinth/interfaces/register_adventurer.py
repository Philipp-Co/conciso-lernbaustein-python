"""A user can register his adventurer.

A adventurers Name must be exactely one character.
"""

#
# ---------------------------------------------------------------------------------------------------------------------
#

from http import HTTPStatus
from json import dumps, loads
from logging import Logger, getLogger
from typing import Any, Dict, Iterable, Optional

from django.http import HttpRequest, HttpResponse
from django.views.generic import View
from labyrinth.domain.registration_service import (
    AdventurerRegistrationResult,
    AdventurerRegistrationService,
)
from rest_framework.serializers import BooleanField, CharField, Serializer

#
# ---------------------------------------------------------------------------------------------------------------------
#


class AdventurerRegistrationRequestSerializer(Serializer):  # type: ignore[misc]
    name = CharField(required=True)
    labyrinth = CharField(required=True)
    pass


#
# ---------------------------------------------------------------------------------------------------------------------
#


class AdventurerRegistrationResponseSerializer(Serializer):  # type: ignore[misc]
    return_value = BooleanField(required=True)
    description = CharField(required=True)
    pass


#
# ---------------------------------------------------------------------------------------------------------------------
#


class RegisterAdventurerView(View):  # type: ignore[misc]
    def __init__(self, *args: Iterable[Any], logger: Optional[Logger] = None, **kwargs: Dict[str, Any]) -> None:
        super().__init__(*args, **kwargs)
        self.__logger: Logger = logger if logger is not None else getLogger(self.__class__.__name__)
        pass

    def __create_response(self, status: int, return_value: bool, description: str) -> HttpResponse:
        return HttpResponse(
            status=status,
            content=dumps(
                AdventurerRegistrationResponseSerializer(
                    data={
                        "return_value": return_value,
                        "description": description,
                    }
                ).initial_data
            ),
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        """Registern an adventurer fur a known labyrinth."""
        serializer: AdventurerRegistrationRequestSerializer = AdventurerRegistrationRequestSerializer(
            data=loads(request.body.decode("utf-8"))
        )
        if not serializer.is_valid():
            return self.__create_response(HTTPStatus.PRECONDITION_FAILED.value, False, "Invalid Request Body.")

        request_body = serializer.data
        result: AdventurerRegistrationResult = AdventurerRegistrationService(
            getLogger("AdventurerRegistration").getChild(AdventurerRegistrationService.__name__)
        ).register_adventurer(
            request_body["name"],
            request_body["labyrinth"],
        )

        return self.__create_response(
            HTTPStatus.OK.value,
            result.return_value,
            result.description,
        )

    pass


#
# ---------------------------------------------------------------------------------------------------------------------
#
