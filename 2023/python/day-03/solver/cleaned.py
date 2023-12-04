# flake8: noqa: F401
import re
from pathlib import Path

from solver.utils import read_lines, get_adjacent

data_path = Path(__file__).parent.parent.absolute() / "data"


class Number:
    def __init__(self, value: str, positions: list(tuple[int, int])):
        self.value = value
        self.positions = positions

    def __repr__(self) -> str:
        return self.value


def solve_1(path: str):
    data = read_lines(path)

    symbol_positions = []
    numbers = []
    for row, line in enumerate(data):
        # Find symbols
        for match in re.finditer(r"[^\s\d\.]", line):
            symbol_positions.append((row, match.start()))

        # Find numbers
        for match in re.finditer(r"\d+", line):
            number = Number(
                value=match.group(),
                positions=[(row, col) for col in range(match.start(), match.end())]
            )
            numbers.append(number)

    result = 0
    for number in numbers:
        adjacent = get_adjacent(*number.positions[0], data, width=len(number.value))
        for pos in adjacent:
            if pos in symbol_positions:
                result += int(number.value)
                break
    
    return result


if __name__ == "__main__":
    answer = solve_1(Path(data_path, "input.txt"))
    print(f"Problem 1: {answer}")