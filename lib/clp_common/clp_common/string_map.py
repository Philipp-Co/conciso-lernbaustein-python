
"""
        +       Crossing/TCrossing/Edge

        | -     hallway/DeadEnd

        S       Start

        E       End
       

        Beispiel fuer eine gueltige Karte:

             +-
             |
        s-+--++
          |   |
          |
         -+-
          |
"""
from typing_extensions import Self
from typing import List
from labyrinth import Element, Empty, DeadEnd, Start, End, Crossing, TCrossing, Edge, Hallway, Orientation
from copy import deepcopy

class StringLabyrinth:

    def __init__(self):
        self.__rows: List[List[str]] = []
        self.__elements: List[List[Element]] = []
        pass
    
    def __parse_minus(self, x: int, y: int) -> Self:
        if self.__rows[y][x-1] == ' ' and self.__rows[y][x+1] == ' ':
            raise ValueError('A "-" can not stand by its own!')
        if self.__rows[y][x-1] == ' ' and self.__rows[y][x+1] != ' ':
            self.__elements[y-1][x-1] = DeadEnd(Orientation.East)
        elif self.__rows[y][x+1] == ' ' and self.__rows[y][x-1] != ' ':
            self.__elements[y-1][x-1] = DeadEnd(Orientation.West)
        elif self.__rows[y+1][x] == ' ' and self.__rows[y-1][x] != ' ':
            self.__elements[y-1][x-1] = DeadEnd(Orientation.North)
        elif self.__rows[y-1][x] == ' ' and self.__rows[y+1][x] != ' ':
            self.__elements[y-1][x-1] = DeadEnd(Orientation.South)
        elif self.__rows[y][x-1] != ' ' and self.__rows[y][x+1] != ' ':
            self.__elements[y-1][x-1] = Hallway(Orientation.West, Orientation.East)
        elif self.__rows[y+1][x] != ' ' and self.__rows[y-1][x] != ' ':
            self.__elements[y-1][x-1] = Hallway(Orientation.North, Orientation.South)
        else:
            raise ValueError
        return self

    def __parse_pipe(self, x: int, y: int) -> Self:
        if self.__rows[y-1][x] == ' ' and self.__rows[y+1][x] == ' ':
            raise ValueError('A "|" can not stand by its own!')
        if self.__rows[y-1][x] == ' ':
            self.__elements[y-1][x-1] = DeadEnd(Orientation.South)
        elif self.__rows[y+1][x] == ' ':
            self.__elements[y-1][x-1] = DeadEnd(Orientation.North)
        else:
            self.__elements[y-1][x-1] = Hallway(Orientation.North, Orientation.South)
        return self

    def __parse_plus(self, x: int, y: int) -> Self:
        t0 = ('S', 'E', '-', '+')
        t1 = ('S', 'E', '|', '+')
        if self.__rows[y][x-1] in t0 and self.__rows[y][x+1] in t0 and self.__rows[y-1][x] in t1 and self.__rows[y+1][x] in t1:
            #
            # This "+" is a Crossing
            #
            self.__elements[y-1][x-1] = Crossing()
        elif self.__rows[y][x-1] in t0 and self.__rows[y+1][x] in t1 and self.__rows[y][x+1] not in t0 and self.__rows[y-1][x] not in t1:
            #
            # Edge
            #
            #   -+
            #    |
            #
            self.__elements[y-1][x-1] = Edge(Orientation.West, Orientation.South)
        elif self.__rows[y][x-1] in t0 and self.__rows[y-1][x] in t1 and self.__rows[y][x+1] not in t0 and self.__rows[y+1][x] not in t1:
            #
            # Edge
            #
            #    |   
            #   -+
            #
            self.__elements[y-1][x-1] = Edge(Orientation.West, Orientation.North)
        elif self.__rows[y][x+1] in t0 and self.__rows[y-1][x] in t1 and self.__rows[y][x-1] not in t0 and self.__rows[y+1][x] not in t1:
            #
            # Edge
            #
            #   |
            #   +- 
            #
            self.__elements[y-1][x-1] = Edge(Orientation.East, Orientation.North)
        elif self.__rows[y][x-1] not in t0 and self.__rows[y+1][x] in t1 and self.__rows[y][x+1] in t0 and self.__rows[y-1][x] not in t1:
            #
            # Edge
            # 
            #   +- 
            #   |
            #
            self.__elements[y-1][x-1] = Edge(Orientation.South, Orientation.East)
        elif self.__rows[y][x-1] in t0 and self.__rows[y][x+1] in t0 and self.__rows[y+1][x] not in t1 and self.__rows[y-1][x] in t1:
            #
            # TCrossing
            #
            #    |
            #   -+-
            #
            #    t0 = ('S', 'E', '-', '+')
            #    t1 = ('S', 'E', '|', '+')
            self.__elements[y-1][x-1] = TCrossing(Orientation.North)
        elif self.__rows[y][x-1] in t0 and self.__rows[y][x+1] in t0 and self.__rows[y+1][x] in t1 and self.__rows[y-1][x] not in t1:
            #
            # TCrossing
            #
            #   -+-
            #    |
            #
            self.__elements[y-1][x-1] = TCrossing(Orientation.South)
        elif self.__rows[y][x-1] not in t0 and self.__rows[y][x+1] in t0 and self.__rows[y+1][x] in t1 and self.__rows[y-1][x] in t1:
            #
            # TCrossing
            #
            #   |
            #   +-
            #   |
            #
            self.__elements[y-1][x-1] = TCrossing(Orientation.East)
        elif self.__rows[y][x-1] in t0 and self.__rows[y][x+1] not in t0 and self.__rows[y+1][x] in t1 and self.__rows[y-1][x] in t1:
            #
            # TCrossing
            #
            #    |
            #   -+
            #    |
            #
            self.__elements[y-1][x-1] = TCrossing(Orientation.West)
        else:
            raise ValueError

        return self

    def __parse_S(self, x: int, y: int) -> Self:
        t0 = ('-', '+')
        t1 = ('|', '+')
        if self.__rows[y][x-1] in t0:
            self.__elements[y-1][x-1] = Start(Orientation.West)
        elif self.__rows[y][x+1] in t0:
            self.__elements[y-1][x-1] = Start(Orientation.East)
        elif self.__rows[y+1][x] in t1:
            self.__elements[y-1][x-1] = Start(Orientation.South)
        elif self.__rows[y-1][x] in t1:
            self.__elements[y-1][x-1] = Start(Orientation.North)
        else:
            raise ValueError
        return self

    def __parse_E(self, x: int, y: int) -> Self:
        t0 = ('-', '+')
        t1 = ('|', '+')
        if self.__rows[y][x-1] in t0:
            self.__elements[y-1][x-1] = End(Orientation.West) 
        elif self.__rows[y][x+1] in t0:
            self.__elements[y-1][x-1] = End(Orientation.East)
        elif self.__rows[y+1][x] in t1:
            self.__elements[y-1][x-1] = End(Orientation.South)
        elif self.__rows[y-1][x] in t1:
            self.__elements[y-1][x-1] = End(Orientation.North)
        else:
            raise ValueError
        return self

    def __update_elements(self) -> Self:
        
        for y in range(1, len(self.__rows)-1):
            for x in range(1, len(self.__rows[y])-1):
                try:
                    match self.__rows[y][x]:
                        case '+':
                            self.__parse_plus(x, y)
                            pass
                        case '-':
                            self.__parse_minus(x, y)
                            pass
                        case '|':
                            self.__parse_pipe(x, y)
                            pass
                        case 'S':
                            self.__parse_S(x, y)
                            pass
                        case 'E':
                            self.__parse_E(x, y)
                            pass
                        case ' ':
                            self.__elements[y-1][x-1] = Empty()
                            pass
                        case '\n':
                            self.__elements[y-1][x-1] = Empty()
                            pass
                        case _:
                            raise ValueError(f'x: {x-1}, y: {y-1} - "{self.__rows[y][x]}" is not valid.')
                except ValueError:
                    print(f'Unabel to parse character at {x-1}, {y-1}')
        return self

    def __update_string_map(self, string: str) -> Self:

        rows = string.split('\n')
        num_rows = len(rows)
        max_col_len = 0
        for row in rows:
            if len(row) > max_col_len:
                max_col_len = len(row)
        
        self.__rows = [[' ' for _j in range(0, max_col_len+2)] for _i in range(0, num_rows+2)]
        self.__elements  = [[Empty() for _j in range(0, max_col_len)] for _i in range(0, num_rows)]
        for i in range(0, len(self.__rows)-3):
            row = rows[i]
            print(f'{i}  : {row}')
            for j in range(0, len(row)):
                self.__rows[i+1][j+1] = rows[i][j]
        return self
    
    def __update(self, string: str) -> Self:
        return self.__update_string_map(string).__update_elements()

    def parse(self, string: str) -> List[List[Element]]:
        return deepcopy(self.__update(string).__elements)
    
    pass

