"""Model for a labyrinth."""
#
# ---------------------------------------------------------------------------------------------------------------------
#
from django.db.models import CASCADE, CharField, ForeignKey, IntegerField, Model

#
# ---------------------------------------------------------------------------------------------------------------------
#


class Labyrinth(Model):  # type: ignore[misc]
    """Each labyrinth consists of multiple tiles.

    The labyrinth is a rectangular map.
    One has random access to its tiles with help of coordinates x and y.
    """

    # the string repraesentation of this instance.
    string_repreesntation = CharField(max_length=4096)
    # the unique instance name.
    name = CharField(max_length=128)

    pass


#
# ---------------------------------------------------------------------------------------------------------------------
#


class LabyrinthTile(Model):  # type: ignore[misc]
    """A tile of a labyrinth."""

    # referenze to the labyrinth.
    labyrinth = ForeignKey(to=Labyrinth, on_delete=CASCADE)
    # tile: S, E, -, |, +
    tile = CharField(max_length=1)
    # tiles neightbors, values are the same as for "tile".
    neighbor_north = CharField(max_length=1)
    neighbor_south = CharField(max_length=1)
    neighbor_east = CharField(max_length=1)
    neighbor_west = CharField(max_length=1)
    # coordinates for this tile.
    x = IntegerField()
    y = IntegerField()

    pass


#
# ---------------------------------------------------------------------------------------------------------------------
#
