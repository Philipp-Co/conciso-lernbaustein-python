from django.db.models import Model, CharField, IntegerField, ForeignKey, CASCADE

class Labyrinth(Model):

    string_repreesntation = CharField(max_length=4096)
    name = CharField(max_length=128)

    pass


class LabyrinthTile(Model):
    
    labyrinth = ForeignKey(to=Labyrinth, on_delete=CASCADE)

    tile = CharField(max_length=1)
    
    neighbor_north = CharField(max_length=1)
    neighbor_south = CharField(max_length=1)
    neighbor_east = CharField(max_length=1)
    neighbor_west = CharField(max_length=1)
    
    x = IntegerField()
    y = IntegerField()

    pass
