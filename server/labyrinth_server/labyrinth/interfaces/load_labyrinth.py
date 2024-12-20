"""A user can register his adventurer.

A adventurers Name must be exactely one character.
"""


from logging import Logger, getLogger
from django.views.generic import View
from django.http import HttpResponse
from typing import Optional

from labyrinth.domain.load_labyrinth import StringLabyrinthLoader, StringLabyrinthLoaderResult
from rest_framework.serializers import Serializer, CharField, BooleanField, ListSerializer
from json import loads, dumps
from http import HTTPStatus

from labyrinth.domain.labyrinth_instances import simple, castle, castle1


class LoadLabyrinthRequestSerializer(Serializer):
    name = CharField(required=True)
    pass

class LoadLabyrinthResponseSerializer(Serializer):
    return_value = BooleanField(required=True)
    description = CharField(required=True)
    pass

class KnownLabyrinthsSerializer(Serializer):
    known_labyrinths = ListSerializer(child=CharField(), default=[])
    pass


class LabyrinthView(View):
    
    def __init__(self, *args, logger: Optional[Logger]=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.__logger: Logger = logger if logger is not None else getLogger(self.__class__.__name__)
        pass

    def __create_response(self, status: int, return_value: bool, description: str) -> HttpResponse:
        return HttpResponse(
            status=status,
            content=dumps(
                LoadLabyrinthResponseSerializer(
                    data={
                        'return_value': return_value,
                        'description': description,
                    }
                ).initial_data 
            )
        )
    
    def get(self, request) -> HttpResponse:
        return HttpResponse (
            status=HTTPStatus.OK.value,
            content=dumps(
                KnownLabyrinthsSerializer(
                    data={
                        'known_labyrinths': StringLabyrinthLoader.known_labyrinths()
                    }
                ).initial_data
            ),
        )


    def post(self, request) -> HttpResponse:
        """Create a Labyrinth."""
        serializer: LoadLabyrinthRequestSerializer = LoadLabyrinthRequestSerializer(
            data=loads(
                request.body.decode('utf-8')
            )
        )
        if not serializer.is_valid():
            return self.__create_response(HTTPStatus.PRECONDITION_FAILED.value, False, 'Invalid Request Body.')
        request_body = serializer.data
        instance: str
        match request_body['name']:
            case 'simple':
                instance = simple
            case 'castle':
                instance = castle
            case 'castle1':
                instance = castle1
            case _:
                return self.__create_response(
                    HTTPStatus.OK.value,
                    False,
                    'Unknown Labyrinth instance.',
                )
        result: StringLabyrinthLoaderResult = StringLabyrinthLoader(
            request_body['name'],
            self.__logger.getChild(StringLabyrinthLoader.__name__),
        ).load_from_string(
            instance
        )

        return self.__create_response(
            HTTPStatus.OK.value,
            result.return_value,
            result.description,
        )

    pass
