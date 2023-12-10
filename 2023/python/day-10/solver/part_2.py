import math
import re
from pprint import pprint
from pathlib import Path
from typing import Self

from solver import utils

data_path = Path(__file__).parent.parent.absolute() / "data"


class Pipe:
    def __init__(self, symbol: str, pos: tuple[int, int], steps: int, parent: Self | None = None):
        self.symbol = symbol
        self.pos = pos
        self.steps = steps
        self.row, self.col = pos
        self.parent = parent
        self.child = None

    def can_connect(self, symbol: str, pos: tuple[int, int]):
        row, col = pos

        if col == self.col:
            if row == self.row - 1:
                return symbol in ("7", "F", "|")

            if row == self.row + 1:
                return symbol in ("J", "L", "|")
            
        if row == self.row:
            if col == self.col - 1:
                return symbol in ("F", "-", "L")
            
            if col == self.col + 1:
                return symbol in ("7", "-", "J")
            

        return False
    
    def __repr__(self) -> str:
        return f"{self.symbol} {self.pos}"
    

def flood_fill_outer(matrix):
    # Flood-fill matrix perimiter
    to_visit = [
        *[(0, col) for col in range(len(matrix[0]))],
        *[(len(matrix) - 1, col) for col in range(len(matrix[0]))],
        *[(row, 0) for row in range(len(matrix))],
        *[(row, len(matrix[0]) - 1) for row in range(len(matrix))],
    ]

    visited = {}
    while to_visit:
        pos = to_visit.pop(0)
        visited[pos] = None

        row, col = pos
        symbol = matrix[row][col]

        if symbol != ".":
            continue
        
        temp = list(matrix[row])
        temp[col] = "O"
        matrix[row] = "".join(temp)

        for new_pos in utils.get_adjacent(*pos, matrix=matrix, include_corners=True):
            if new_pos in visited or new_pos in to_visit:
                continue

            to_visit.append(new_pos)

    for line in matrix:
        print(line)


def shoelace_area(points: list[tuple[int, int]]):
    x_values = [point[1] for point in points]
    y_values = [point[0] for point in points]

    p_1 = sum(
        x * y for x, y in zip(x_values, [*y_values[1:], y_values[0]])
    )

    p_2 = sum(
        x * y for x, y in zip([*x_values[1:], x_values[0]], y_values)
    )

    return 0.5 * abs(p_1 - p_2)




def solve(path: str):
    data = utils.read_lines(path)

    flood_fill_outer(data)

    # Find Start position
    start_pipe = None
    for row, line in enumerate(data):
        col  = line.find("S")
        if col != -1:
            start_pipe = Pipe(symbol="S", pos=(row, col), steps=0)


    visited = {}
    to_visit = [start_pipe]
    while to_visit:
        pipe = to_visit.pop(0)
        visited[pipe.pos] = None

        for row, col in utils.get_adjacent(*pipe.pos, matrix=data, include_corners=False):
            new_pos = (row, col)
            symbol = data[row][col]

            if new_pos in visited or new_pos in to_visit:
                continue

            if not pipe.can_connect(symbol, pos=new_pos):
                continue

            new_pipe = Pipe(symbol=symbol, pos=(row, col), steps=pipe.steps + 1)
            pipe.child = new_pipe
            to_visit.append(new_pipe)
            break

    points = []
    pipe = start_pipe
    while pipe.child is not None:
        points.append(pipe.pos)
        pipe = pipe.child
    
    polygon_area = shoelace_area(points)
    print(polygon_area)

    for row, line in enumerate(data):
        for res in re.finditer(r"\.", line):
            col = res.start()

            p = (row, col)

            new_area = shoelace_area([*points, p])

            print(p, new_area)


    return 10


def point_distance(p1, p2):
    x_value = (p2[1] - p1[1]) ** 2
    y_value = (p2[0] - p1[0]) ** 2
    return math.sqrt(x_value + y_value)

if __name__ == "__main__":
    #answer = solve(Path(data_path, "input.txt"))
    answer = solve(Path(data_path, "example_2.txt"))
    if answer is not None:
        print(f"Problem 2: {answer}")