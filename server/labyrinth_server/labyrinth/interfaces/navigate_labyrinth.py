"""A user can navigate his adventurer through the labyrinth.

Directions allowed:
    - north
    - south
    - east
    - west

The current state of the labyrinth can be retreaved.
"""
#
# ---------------------------------------------------------------------------------------------------------------------
#

from http import HTTPStatus
from json import dumps, loads
from logging import Logger, getLogger
from typing import Any, Dict, Iterable, Optional

from clp_common.labyrinth import Orientation
from django.http import HttpRequest, HttpResponse
from django.views.generic import View
from labyrinth.domain.navigate_labyrinth import LabyrinthNavigator
from rest_framework.serializers import BooleanField, CharField, Serializer

#
# ---------------------------------------------------------------------------------------------------------------------
#


class WhereAmIRequestSerializer(Serializer):  # type: ignore[misc]
    pass


#
# ---------------------------------------------------------------------------------------------------------------------
#


class WhereAmIResponseSerializer(Serializer):  # type: ignore[misc]
    return_value = BooleanField(required=True)
    description = CharField(required=True)
    current_tile = CharField(required=True)
    north_tile = CharField(required=True)
    east_tile = CharField(required=True)
    south_tile = CharField(required=True)
    west_tile = CharField(required=True)
    pass


#
# ---------------------------------------------------------------------------------------------------------------------
#


class MoveRequestSerializer(Serializer):  # type: ignore[misc]
    direction = CharField(required=True)
    pass


#
# ---------------------------------------------------------------------------------------------------------------------
#


class MoveResponseSerializer(Serializer):  # type: ignore[misc]
    return_value = BooleanField(required=True)
    description = CharField(required=True)
    solved = BooleanField(required=True)
    pass


#
# ---------------------------------------------------------------------------------------------------------------------
#


class NavigateLabyrinthView(View):  # type: ignore[misc]
    def __init__(self, *args: Iterable[Any], logger: Optional[Logger] = None, **kwargs: Dict[str, Any]) -> None:
        super().__init__(*args, **kwargs)
        self.__logger: Logger = logger if logger is not None else getLogger(self.__class__.__name__)
        pass

    def get(self, request: HttpRequest, adventurer_name: str) -> HttpResponse:
        """Receive information about the given adventurers position inside the labyrinth."""
        return HttpResponse(
            status=HTTPStatus.OK,
            content=dumps(
                WhereAmIResponseSerializer(
                    data=LabyrinthNavigator(logger=self.__logger.getChild(LabyrinthNavigator.__name__))
                    .where_am_i(adventurer_name=adventurer_name)
                    .to_json_serializable()
                ).initial_data
            ),
        )

    def post(self, request: HttpRequest, adventurer_name: str) -> HttpResponse:
        """Let the given adventurer make his move."""
        serializer: MoveRequestSerializer = MoveRequestSerializer(data=loads(request.body.decode("utf-8")))
        if serializer.is_valid():
            data = serializer.data
            orientation: Orientation = Orientation[data["direction"]]
            return HttpResponse(
                content=dumps(
                    MoveResponseSerializer(
                        data=LabyrinthNavigator(logger=self.__logger.getChild(LabyrinthNavigator.__name__))
                        .move(
                            adventurer_name=adventurer_name,
                            orientation=orientation,
                        )
                        .to_json_serializable()
                    ).initial_data
                )
            )
        return HttpResponse(
            status=HTTPStatus.PRECONDITION_FAILED,
            content=dumps(
                MoveResponseSerializer(
                    data={
                        "return_value": False,
                        "solved": False,
                        "description": "Unable to parse Request data.",
                    }
                ).initial_data
            ),
        )

    pass


#
# ---------------------------------------------------------------------------------------------------------------------
#
