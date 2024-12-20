"""A user can register his adventurer.

A adventurers Name must be exactely one character.
"""


from logging import Logger, getLogger
from django.views.generic import View
from django.http import HttpResponse
from logging import getLogger, Logger
from typing import Optional

from labyrinth.domain.registration_service import AdventurerRegistrationService, AdventurerRegistrationResult
from rest_framework.serializers import Serializer, CharField, BooleanField
from json import loads, dumps
from http import HTTPStatus


class AdventurerRegistrationRequestSerializer(Serializer):
    name = CharField(required=True)
    labyrinth = CharField(required=True) 
    pass

class AdventurerRegistrationResponseSerializer(Serializer):
    return_value = BooleanField(required=True)
    description = CharField(required=True)
    pass

class RegisterAdventurerView(View):
    
    def __init__(self, *args, logger: Optional[Logger]=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.__logger: Logger = logger if logger is not None else getLogger(self.__class__.__name__)
        pass

    def __create_response(self, status: int, return_value: bool, description: str) -> HttpResponse:
        return HttpResponse(
            status=status,
            content=dumps(
                AdventurerRegistrationResponseSerializer(
                    data={
                        'return_value': return_value,
                        'description': description,
                    }
                ).initial_data 
            )
        )


    def post(self, request) -> HttpResponse:
        serializer: AdventurerRegistrationRequestSerializer = AdventurerRegistrationRequestSerializer(
            data=loads(
                request.body.decode('utf-8')
            )
        )
        if not serializer.is_valid():
            return self.__create_response(HTTPStatus.PRECONDITION_FAILED.value, False, 'Invalid Request Body.')

        request_body = serializer.data
        result: AdventurerRegistrationResult = AdventurerRegistrationService(
            getLogger('AdventurerRegistration').getChild(AdventurerRegistrationService.__name__)
        ).register_adventurer(
            request_body['name'],
            request_body['labyrinth'],
        )

        return self.__create_response(
            HTTPStatus.OK.value,
            result.return_value,
            result.description,
        )

    pass
