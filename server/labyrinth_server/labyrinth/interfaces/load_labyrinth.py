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
from labyrinth.domain.authentication.token_user import LabyrinthTokenUser
from labyrinth.domain.authentication.usage_allowed import UsageAllowed
from labyrinth.domain.labyrinth_instances import castle, castle1, simple
from labyrinth.domain.load_labyrinth import (
    StringLabyrinthLoader,
    StringLabyrinthLoaderResult,
)
from rest_framework.decorators import permission_classes
from rest_framework.serializers import (
    BooleanField,
    CharField,
    ListSerializer,
    Serializer,
)
from rest_framework.views import APIView

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


class LabyrinthView(APIView):  # type: ignore[misc]
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

    @permission_classes([UsageAllowed])  # type: ignore[misc]
    def get(self, request: HttpRequest) -> HttpResponse:
        """List the known labyrinths.

        This are the labyrinths an adventurer can register for and then solve.
        """
        user = request.user
        if not isinstance(user, LabyrinthTokenUser):
            return self.__create_response(
                HTTPStatus.UNAUTHORIZED.value, return_value=False, description="Bitte Authentifizieren!"
            )
        if not user.is_allowed_to_solve():
            return self.__create_response(
                HTTPStatus.UNAUTHORIZED.value,
                return_value=False,
                description=f"You are allowed: {user.is_allowed_to_solve()}",
            )
        return HttpResponse(
            status=HTTPStatus.OK.value,
            content=dumps(
                KnownLabyrinthsSerializer(
                    data={"known_labyrinths": StringLabyrinthLoader.known_labyrinths()}
                ).initial_data
            ),
        )

    @permission_classes([UsageAllowed])  # type: ignore[misc]
    def post(self, request: HttpRequest) -> HttpResponse:
        """Create a Labyrinth."""
        try:
            user = request.user
            if not isinstance(user, LabyrinthTokenUser) or (
                isinstance(user, LabyrinthTokenUser) and not user.is_allowed_to_load_new()
            ):
                return HttpResponse(
                    status=HTTPStatus.UNAUTHORIZED.value,
                )
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
        except Exception as e:
            self.__logger.exception(e)
            return self.__create_response(
                HTTPStatus.INTERNAL_SERVER_ERROR.value,
                False,
                "Internal Server Error.",
            )

    pass


#
# ---------------------------------------------------------------------------------------------------------------------
#
