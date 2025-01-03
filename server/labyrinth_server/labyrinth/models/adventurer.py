"""Model for an adventurer."""

# ---------------------------------------------------------------------------------------------------------------------
#
from django.db.models import CASCADE, CharField, ForeignKey, Model

#
from labyrinth.models.labyrinth import Labyrinth, LabyrinthTile

#
# ---------------------------------------------------------------------------------------------------------------------
#


class Adventurer(Model):  # type: ignore[misc]
    """An adventurer."""

    # uniquely identify an adventurer who is solving a known labyrinth.
    name = CharField(max_length=32, unique=True)

    # reference to the labyrinth which is solved by this adventurer.
    labyrinth = ForeignKey(to=Labyrinth, on_delete=CASCADE, null=True, default=None)
    # current tile the adventurer is standing on.
    current_tile = ForeignKey(to=LabyrinthTile, on_delete=CASCADE, null=True, default=None)

    pass


#
# ---------------------------------------------------------------------------------------------------------------------
#
