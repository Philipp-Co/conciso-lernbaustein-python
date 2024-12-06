"""Implementation of a Client Factory."""
# ---------------------------------------------------------------------------------------------------------------------
from interfaces.iclient import IClient
from logging import getLogger, Logger
from typing import Dict
from interfaces.default_client import DefaultClient
import importlib
# ---------------------------------------------------------------------------------------------------------------------

class ClientFactory:
    """Implements a factory which generates client by class names."""
    def __init__(self, logger: Logger):
        self.__logger: Logger = logger
        pass

    def create(self, module_name: str, class_name: str) -> IClient:
        """Creates a client.

        Loads the class f'{module_name}.{class_name}', initializes and returns the object.
        
        Raises:
            ValueError: If the class which was loaded is no IClient this function will raise an Error.
        """
        self.__logger.info(f'Import {module_name}.{class_name}')
        module = importlib.import_module(module_name)
        class_instance = getattr(module, class_name)
        object: IClient = class_instance()
        if not isinstance(object, IClient):
            raise ValueError(f'Die angegebene Klasse {module_name}.{class_name} ist kein IClient!')
        return object.set_logger(
            self.__logger.getChild(class_name)
        )

    pass
# ---------------------------------------------------------------------------------------------------------------------
