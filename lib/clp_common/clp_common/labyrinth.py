
from abc import ABC, abstractmethod
from typing_extensions import Self
from enum import IntEnum
from typing import List


class Orientation(IntEnum):

    North = 0,
    East = 1,
    South = 2,
    West = 3,

    pass


class Canvas:
    
    def __init__(self, width: int, height: int):
        self.__tiles = []
        for i in range(0, height):
            self.__tiles.append([])
            for j in range(0, width):
                self.__tiles[i].append(' ')
        pass

    def to_string(self) -> str:
        result = ''
        for i in range(0, len(self.__tiles)):
            for j in range(0, len(self.__tiles[i])):
                result = result + self.__tiles[i][j]
            result = result + '\n'
        return result
    
    def width(self) -> int:
        return len(self.__tiles[0])

    def height(self) -> int:
        return len(self.__tiles)

    def set(self, x: int, y: int, c: str) -> Self:
        self.__tiles[y][x] = c
        return self 

    pass

class Renderable(ABC):
    @abstractmethod
    def render(self, c: Canvas):
        pass
    pass

class Adventurer(Renderable):
    
    def __init__(self, symbol: str, x: int=0, y: int=0):
        super().__init__()
        self.__x: int = x
        self.__y: int = y
        if len(symbol) != 1:
            raise ValueError(f'The Symbol for an Adventurer has to be one Character only!')
        self.__symbol = symbol
        pass
    
    def get_x(self) -> int:
        return self.__x

    def get_y(self) -> int:
        return self.__y

    
    def set_x(self, x: int) -> Self:
        self.__x = x
        return self

    def set_y(self, y: int) -> Self:
        self.__y = y
        return self

    def render(self, c: Canvas):
        c.set(self.__x * 9 + 4, self.__y * 5 + 2, self.__symbol)
        return self

    pass

class Element(Renderable):
    
    def __init__(self, x: int=0, y: int=0):
        self.x = x
        self.y = y
        pass
    
    def set_coordinates(self, x: int, y: int) -> Self:
        self.x = x
        self.y = y
        return self

    def tile_width(self) -> int:
        return 9

    def tile_height(self) -> int:
        return 5

    def transform_x(self, x: int) -> int:
        return x * self.tile_width()

    def transform_y(self, y: int) -> int:
        return y * self.tile_height()

    def render_string_tile(self, stringtile: str, c: Canvas) -> Self:
        x = self.transform_x(self.x)
        y = self.transform_y(self.y)
        for row in range(0, self.tile_height()):
            for col in range(0, self.tile_width()):
                c.set(x + col, y + row, stringtile[row * self.tile_width() + col]) 
        return self
    pass

class Empty(Element):

    def __init__(self, x: int=0, y: int=0):
        super().__init__(x, y)
        pass
    def render(self, c: Canvas) -> Self:
        return self
    pass

class TCrossing(Element):
    def __init__(self, ino: Orientation, x: int=0, y: int=0):
        super().__init__(x, y)
        self.__in_orientation: Orientation = ino
        pass

    def render(self, c: Canvas) -> Self:
        lookup = {
            Orientation.North:
                "  |   |  "\
                "--+   +--"\
                "         "\
                "---------"\
                "         ",
            Orientation.East:
                "  |   |  "\
                "  |   +--"\
                "  |      "\
                "  |   +--"\
                "  |   |  ",
            Orientation.South:
                "         "\
                "---------"\
                "         "\
                "--+   +--"\
                "  |   |  ",
            Orientation.West:
                "  |   |  "\
                "--+   |  "\
                "      |  "\
                "--+   |  "\
                "  |   |  ",
        }

        return self.render_string_tile(lookup[self.__in_orientation], c)

    pass

class Crossing(Element):
    
    def __init__(self, x: int=0, y: int=0):
        super().__init__(x, y)
        pass

    def render(self, c: Canvas) -> Self:
        tile: str = \
            "  |   |  "\
            "--+   +--"\
            "         "\
            "--+   +--"\
            "  |   |  "
        return self.render_string_tile(tile, c)
    pass

class Edge(Element):
    def __init__(
            self, 
            ino: Orientation, outo: Orientation,
            x: int=0, y: int=0, 
        ):
        super().__init__(x, y)
        self.__in_orientation: Orientation = ino
        self.__out_orientation: Orientation = outo
        pass

    def render(self, c: Canvas):
        lookup = {
            (Orientation.South, Orientation.West): 
                "         "\
                "------+  "\
                "      |  "\
                "--+   |  "\
                "  |   |  ",
            (Orientation.East, Orientation.South): 
                "         "\
                "  +------"\
                "  |      "\
                "  |   +--"\
                "  |   |  ",
            (Orientation.North, Orientation.East): 
                "  |   |  "\
                "  |   +--"\
                "  |      "\
                "  +------"\
                "         ",
            (Orientation.North, Orientation.West): 
                "  |   |  "\
                "--+   |  "\
                "      |  "\
                "------+  "\
                "         ",
        }
        key = tuple(sorted((self.__in_orientation, self.__out_orientation))) 
        tile: str = lookup[key]
        return self.render_string_tile(tile, c)

    pass

class Hallway(Element):
    def __init__(
            self, 
            ino: Orientation, outo: Orientation,
            x: int=0, y: int=0, 
        ):
        super().__init__(x, y)
        self.__in_orientation: Orientation = ino
        self.__out_orientation: Orientation = outo
        pass
    
    def render(self, c: Canvas):
        lookup = {
            (Orientation.North, Orientation.South):
                "  |   |  "\
                "  |   |  "\
                "  |   |  "\
                "  |   |  "\
                "  |   |  ",
            (Orientation.South, Orientation.North):
                "  |   |  "\
                "  |   |  "\
                "  |   |  "\
                "  |   |  "\
                "  |   |  ",
            (Orientation.East, Orientation.West):
                "         "\
                "---------"\
                "         "\
                "---------"\
                "         ",
            (Orientation.West, Orientation.East):
                "         "\
                "---------"\
                "         "\
                "---------"\
                "         ",
        }
        tile: str = lookup[(self.__in_orientation, self.__out_orientation)]
        return self.render_string_tile(tile, c)
    pass

class DeadEnd(Element):

    def __init__(self, ino: Orientation, x: int=0, y: int=0):
        super().__init__(x, y)
        self.__orientation: Orientation = ino
        pass

    def render(self, c: Canvas):
        lookup = {
            Orientation.North:
                "  |   |  "\
                "  |   |  "\
                "  |   |  "\
                "  +---+  "\
                "         ",
            Orientation.East:
                "         "\
                "  +------"\
                "  |      "\
                "  +------"\
                "         ",
            Orientation.South:
                "         "\
                "  +---+  "\
                "  |   |  "\
                "  |   |  "\
                "  |   |  ",
            Orientation.West:
                "         "\
                "-------+ "\
                "       | "\
                "-------+ "\
                "         ",
        }
        return self.render_string_tile(lookup[self.__orientation], c)
    pass

class Start(Element):

    def __init__(self, ino: Orientation, x: int=0, y: int=0):
        super().__init__(x, y)
        self.__orientation: Orientation = ino
        pass

    def render(self, c: Canvas):
        lookup = {
            Orientation.North:
                "  |   |  "\
                "  |   |  "\
                "  | S |  "\
                "  +---+  "\
                "         ",
            Orientation.East:
                "         "\
                "  +------"\
                "  |S     "\
                "  +------"\
                "         ",
            Orientation.South:
                "         "\
                "  +---+  "\
                "  | S |  "\
                "  |   |  "\
                "  |   |  ",
            Orientation.West:
                "         "\
                "-------+ "\
                "      S| "\
                "-------+ "\
                "         ",
        }
        return self.render_string_tile(lookup[self.__orientation], c)
    pass

class End(Element):

    def __init__(self, ino: Orientation, x: int=0, y: int=0):
        super().__init__(x, y)
        self.__orientation: Orientation = ino
        pass

    def render(self, c: Canvas):
        lookup = {
            Orientation.North:
                "  |   |  "\
                "  |   |  "\
                "  | E |  "\
                "  +---+  "\
                "         ",
            Orientation.East:
                "         "\
                "  +------"\
                "  |E     "\
                "  +------"\
                "         ",
            Orientation.South:
                "         "\
                "  +---+  "\
                "  | E |  "\
                "  |   |  "\
                "  |   |  ",
            Orientation.West:
                "         "\
                "-------+ "\
                "      E| "\
                "-------+ "\
                "         ",
        }
        return self.render_string_tile(lookup[self.__orientation], c)
    pass

class Labyrinth:

    def __init__(self):
        self.__matrix: List[List[int]] = []
        self.__adventurer = {}
        pass
    
    def set_elements(
        self, 
        elements: List[List[Element]],
    ) -> Self:
        self.__matrix: List[List[int]] = [
            [Empty() for _x in range(0, len(elements[0]))] for _y in range(0, len(elements))
        ]
        for i in range(0, len(elements)):
            for j in range(0, len(elements[i])):
                self.__matrix[i][j] = elements[i][j].set_coordinates(j, i)
        return self
    
    def add_adventurer(self, adventurer: str) -> Self:
        self.__adventurer[adventurer] = Adventurer(adventurer[0])
        for i in range(0, len(self.__matrix)):
            for j in range(0, len(self.__matrix[0])):
                if isinstance(self.__matrix[i][j], Start):
                    self.__adventurer[adventurer].set_x(j).set_y(i)
        return self
    
    def move_adventurer(self, adventurer: str, direction: Orientation) -> Self:
        a: Adventurer = self.__adventurer[adventurer]
        x: int = a.get_x()
        y: int = a.get_y()
        
        match direction:
            case Orientation.North:
                if isinstance(self.__matrix[y-1][x], Empty):
                    raise IndexError
                a.set_y(y-1) 
                pass
            case Orientation.South:
                if isinstance(self.__matrix[y+1][x], Empty):
                    raise IndexError
                a.set_y(y+1) 
                pass
            case Orientation.West:
                if isinstance(self.__matrix[y][x-1], Empty):
                    raise IndexError
                a.set_x(x-1) 
                pass
            case Orientation.East:
                if isinstance(self.__matrix[y][x+1], Empty):
                    raise IndexError
                a.set_x(x+1) 
                pass
            case _:
                raise KeyError
        return self

    def render(self) -> Self:
        canvas: Canvas = Canvas(len(self.__matrix[0]) * 9, len(self.__matrix) * 5)
        for i in range(0, len(self.__matrix)):
            for j in range(0, len(self.__matrix[i])):
                self.__matrix[i][j].set_coordinates(j, i).render(canvas)
        
        for key in self.__adventurer:
            self.__adventurer[key].render(canvas)
        print('---------------------')
        print(
            canvas.to_string()
        )
        print('---------------------')
        return self

    pass

