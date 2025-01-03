"""Register an adventurer."""

# ---------------------------------------------------------------------------------------------------------------------
#
from dataclasses import dataclass

#
from logging import Logger

from django.db import IntegrityError
from labyrinth.models.adventurer import Adventurer
from labyrinth.models.labyrinth import Labyrinth, LabyrinthTile

#
# ---------------------------------------------------------------------------------------------------------------------
#


@dataclass
class AdventurerRegistrationResult:
    """Dataclass."""

    return_value: bool
    description: str
    pass


#
# ---------------------------------------------------------------------------------------------------------------------
#


class AdventurerRegistrationService:
    """Register an adventurer."""

    def __init__(self, logger: Logger):
        """C'tor."""
        self.__logger: Logger = logger
        pass

    def __find_start_tile(self, labyrinth: Labyrinth) -> LabyrinthTile:
        """Find the start tile (S) of the labyrinth and return its tile."""
        return LabyrinthTile.objects.get(  # type: ignore[no-any-return]
            labyrinth=labyrinth,
            tile="S",
        )

    def register_adventurer(self, name: str, labyrinth_name: str) -> AdventurerRegistrationResult:
        """Register an adventurer by his name.

        If the adventurer was registred he is assigned to the start tile.
        From now on, the adventurer can make his moves.
        """
        if len(name) > 32 or len(name) < 1:
            return AdventurerRegistrationResult(
                False,
                f'Name "{name}" to long, 1 < length(name) <= 32.',
            )

        try:
            labyrinth: Labyrinth = Labyrinth.objects.get(name=labyrinth_name)
            adventurer: Adventurer = Adventurer()
            adventurer.name = name
            adventurer.labyrinth = labyrinth
            adventurer.current_tile = self.__find_start_tile(labyrinth=labyrinth)
            adventurer.save()
        except IntegrityError as e:
            self.__logger.exception(e)
            return AdventurerRegistrationResult(
                False,
                "A Adventurer with the given Name or Symbol already exists. Try another Name and Symbol.",
            )

        self.__logger.info(f'Register Adventurer "{name}"...')
        return AdventurerRegistrationResult(True, "Ok.")

    pass


#
# ---------------------------------------------------------------------------------------------------------------------
#
