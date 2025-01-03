"""Navigate the labyrinth."""

# ---------------------------------------------------------------------------------------------------------------------
#
from dataclasses import dataclass

#
from logging import Logger
from typing import Any, Dict

from clp_common.labyrinth import Orientation
from labyrinth.models.adventurer import Adventurer
from labyrinth.models.labyrinth import LabyrinthTile

#
# ---------------------------------------------------------------------------------------------------------------------
#


@dataclass
class AdventurerPosition:
    """Dataclass."""

    return_value: bool
    solved: bool
    description: str
    current_tile: str
    north_tile: str
    east_tile: str
    south_tile: str
    west_tile: str

    def to_json_serializable(self) -> Dict[str, Any]:
        """Convert this instance to a JSON convertable object."""
        return {
            "return_value": self.return_value,
            "solved": self.solved,
            "description": self.description,
            "current_tile": self.current_tile,
            "north_tile": self.north_tile,
            "east_tile": self.east_tile,
            "south_tile": self.south_tile,
            "west_tile": self.west_tile,
        }

    pass


#
# ---------------------------------------------------------------------------------------------------------------------
#


@dataclass
class AdventurerMoveResult:
    """Dataclass."""

    return_value: bool
    solved: bool
    description: str

    def to_json_serializable(self) -> Dict[str, Any]:
        """Convert this instance to a JSON convertable object."""
        return {
            "return_value": self.return_value,
            "solved": self.solved,
            "description": self.description,
        }

    pass


#
# ---------------------------------------------------------------------------------------------------------------------
#


class LabyrinthNavigator:
    """Navigate through the labyrinth."""

    def __init__(self, logger: Logger):
        """C'tor."""
        self.__logger: Logger = logger
        pass

    def where_am_i(self, adventurer_name: str) -> AdventurerPosition:
        """Get information about an adeventurers current position inside his labyrinth."""
        try:
            adventurer = Adventurer.objects.get(name=adventurer_name)
            current_tile: LabyrinthTile = adventurer.current_tile
            return AdventurerPosition(
                return_value=True,
                solved=current_tile.tile == "E",
                description="Ok.",
                current_tile=current_tile.tile,
                north_tile=current_tile.neighbor_north,
                east_tile=current_tile.neighbor_east,
                south_tile=current_tile.neighbor_south,
                west_tile=current_tile.neighbor_west,
            )
        except:  # noqa: E722
            return AdventurerPosition(
                return_value=False,
                solved=False,
                description="Unknown Adventurer...",
                current_tile=" ",
                north_tile=" ",
                east_tile=" ",
                south_tile=" ",
                west_tile=" ",
            )

    def move(self, adventurer_name: str, orientation: Orientation) -> AdventurerMoveResult:
        """Make a move."""
        try:
            # get adventurer
            adventurer: Adventurer = Adventurer.objects.get(name=adventurer_name)
            tile: LabyrinthTile = adventurer.current_tile

            # check neighboring tiles
            delta_x: int = 0
            delta_y: int = 0
            neighbor: str
            match orientation:
                case Orientation.North:
                    neighbor = tile.neighbor_north
                    delta_y = -1
                    pass
                case Orientation.East:
                    neighbor = tile.neighbor_east
                    delta_x = 1
                    pass
                case Orientation.South:
                    neighbor = tile.neighbor_south
                    delta_y = 1
                    pass
                case Orientation.West:
                    neighbor = tile.neighbor_west
                    delta_x = -1
                    pass
                case _:
                    raise ValueError("Unknown orientation.")

            if neighbor not in {"-", "|", "+", "S", "E"}:
                return AdventurerMoveResult(
                    return_value=False,
                    solved=False,
                    description="You can not step on this tile.",
                )

            # find next tile.
            adventurer.current_tile = LabyrinthTile.objects.get(
                labyrinth=adventurer.labyrinth,
                x=adventurer.current_tile.x + delta_x,
                y=adventurer.current_tile.y + delta_y,
            )
            self.__logger.info(
                f"Adventurer {adventurer_name} steps on tile x: {adventurer.current_tile.x},"
                f" y: {adventurer.current_tile.y} ->  {adventurer.current_tile.tile}"
            )
            adventurer.save()
            return AdventurerMoveResult(
                return_value=True,
                solved="E" == adventurer.current_tile.tile,
                description="Ok.",
            )
        except Exception as e:
            self.__logger.exception(e)
            return AdventurerMoveResult(
                return_value=False,
                solved=False,
                description="Exception.",
            )

    pass


#
# ---------------------------------------------------------------------------------------------------------------------
#
