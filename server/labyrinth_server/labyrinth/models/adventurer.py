from django.db.models import Model, CharField, IntegerField, ForeignKey, CASCADE
from labyrinth.models.labyrinth import LabyrinthTile, Labyrinth

class Adventurer(Model):

    name = CharField(max_length=32, unique=True)

    labyrinth = ForeignKey(to=Labyrinth, on_delete=CASCADE, null=True, default=None)
    current_tile = ForeignKey(to=LabyrinthTile, on_delete=CASCADE, null=True, default=None)

    pass
