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
from labyrinth.domain.labyrinth_instances import castle, castle1, simple
from labyrinth.domain.load_labyrinth import (
    StringLabyrinthLoader,
    StringLabyrinthLoaderResult,
)
from rest_framework.serializers import (
    BooleanField,
    CharField,
    ListSerializer,
    Serializer,
)

#
# ---------------------------------------------------------------------------------------------------------------------
#


class LoadLabyrinthRequestSerializer(Serializer):  # type: ignore[misc]
    name = CharField(required=True)
    pass


#
# ---------------------------------------------------------------------------------------------------------------------
#


class LoadLabyrinthResponseSerializer(Serializer):  # type: ignore[misc]
    return_value = BooleanField(required=True)
    description = CharField(required=True)
    pass


#
# ---------------------------------------------------------------------------------------------------------------------
#


class KnownLabyrinthsSerializer(Serializer):  # type: ignore[misc]
    known_labyrinths = ListSerializer(child=CharField(), default=[])
    pass


#
# ---------------------------------------------------------------------------------------------------------------------
#


class LabyrinthView(View):  # type: ignore[misc]
    def __init__(self, *args: Iterable[Any], logger: Optional[Logger] = None, **kwargs: Dict[str, Any]) -> None:
        super().__init__(*args, **kwargs)
        self.__logger: Logger = logger if logger is not None else getLogger(self.__class__.__name__)
        pass

    def __create_response(self, status: int, return_value: bool, description: str) -> HttpResponse:
        return HttpResponse(
            status=status,
            content=dumps(
                LoadLabyrinthResponseSerializer(
                    data={
                        "return_value": return_value,
                        "description": description,
                    }
                ).initial_data
            ),
        )

    def get(self, request: HttpRequest) -> HttpResponse:
        """List the known labyrinths.

        This are the labyrinths an adventurer can register for and then solve.
        """
        return HttpResponse(
            status=HTTPStatus.OK.value,
            content=dumps(
                KnownLabyrinthsSerializer(
                    data={"known_labyrinths": StringLabyrinthLoader.known_labyrinths()}
                ).initial_data
            ),
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        """Create a Labyrinth."""
        serializer: LoadLabyrinthRequestSerializer = LoadLabyrinthRequestSerializer(
            data=loads(request.body.decode("utf-8"))
        )
        if not serializer.is_valid():
            return self.__create_response(HTTPStatus.PRECONDITION_FAILED.value, False, "Invalid Request Body.")
        request_body: Dict[str, Any] = serializer.data
        instance: str
        match request_body["name"]:
            case "simple":
                instance = simple
                pass
            case "castle":
                instance = castle
                pass
            case "castle1":
                instance = castle1
                pass
            case _:
                return self.__create_response(
                    HTTPStatus.OK.value,
                    False,
                    "Unknown Labyrinth instance.",
                )
        result: StringLabyrinthLoaderResult = StringLabyrinthLoader(
            request_body["name"],
            self.__logger.getChild(StringLabyrinthLoader.__name__),
        ).load_from_string(instance)

        return self.__create_response(
            HTTPStatus.OK.value,
            result.return_value,
            result.description,
        )

    pass


#
# ---------------------------------------------------------------------------------------------------------------------
#
