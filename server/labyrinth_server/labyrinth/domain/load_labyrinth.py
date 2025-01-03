"""Load labyrinths into memory."""


# ---------------------------------------------------------------------------------------------------------------------
#
from dataclasses import dataclass

#
from logging import Logger
from typing import List

from clp_common.string_map import Element, StringLabyrinth
from labyrinth.models.labyrinth import Labyrinth as LabyrinthModel
from labyrinth.models.labyrinth import LabyrinthTile

#
# ---------------------------------------------------------------------------------------------------------------------
#


@dataclass
class StringLabyrinthLoaderResult:
    """Simple Dataclass."""

    return_value: bool
    description: str
    pass


#
# ---------------------------------------------------------------------------------------------------------------------
#


class StringLabyrinthLoader:
    """Load a labyrinth from a given String."""

    def __init__(self, name: str, logger: Logger):
        """C'tor."""
        self.__logger: Logger = logger
        self.__map: str = ""
        self.__name: str = name
        self.__elements: List[List[Element]] = []
        pass

    @staticmethod
    def known_labyrinths() -> List[str]:
        """Returns a list with known labyrinths.

        A labyrinth is known if it was loaded and then stored into the database.
        """
        return [labyrinth.name for labyrinth in LabyrinthModel.objects.all()]

    def load_from_string(self, data: str) -> StringLabyrinthLoaderResult:
        """Load a labyrinth from a given string."""
        try:
            self.__elements = StringLabyrinth(self.__logger.getChild(StringLabyrinth.__name__)).parse(data)
            self.__map = data
            if self.write_to_database():
                return StringLabyrinthLoaderResult(
                    True,
                    "Ok.",
                )
            else:
                return StringLabyrinthLoaderResult(
                    False,
                    "Unable to write to Database.",
                )

        except Exception as e:
            self.__logger.exception(e)
            return StringLabyrinthLoaderResult(False, "A Exception has occured.")
        return StringLabyrinthLoaderResult(True, "Ok.")

    def write_to_database(self) -> bool:
        """Write internals of this instance into the database."""
        if len(LabyrinthModel.objects.filter(name=self.__name)) > 0:
            return True

        labyrinth: LabyrinthModel = LabyrinthModel()
        labyrinth.string_repreesntation = self.__map
        labyrinth.name = self.__name
        labyrinth.save()

        lmap: List[str] = self.__map.split("\n")
        # The Last line is possibly empty...
        if len(lmap[-1]) == 0:
            lmap = lmap[0 : len(lmap) - 1]
        self.__logger.info(f"Save Map ({len(lmap)}):")
        for line in lmap:
            self.__logger.info(line)

        row: int
        col: int
        for row in range(0, len(lmap)):
            for col in range(0, len(lmap[row])):
                e: LabyrinthTile = LabyrinthTile()
                e.labyrinth = labyrinth
                e.tile = lmap[row][col]
                if (row - 1) >= 0:
                    e.neighbor_north = lmap[row - 1][col]
                if (col + 1) < len(lmap[row]):
                    e.neighbor_east = lmap[row][col + 1]
                if (row + 1) < len(lmap):
                    e.neighbor_south = lmap[row + 1][col]
                if (col - 1) >= 0:
                    e.neighbor_west = lmap[row][col - 1]
                e.y = row
                e.x = col
                e.save()

        return True

    pass


#
# ---------------------------------------------------------------------------------------------------------------------
#
