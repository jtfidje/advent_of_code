# flake8: noqa: F401

from pathlib import Path

from solver.utils import (
    json_print,
    read_lines,
    read_numbers,
    sliding_window
)

data_path = Path(__file__).parent.parent.absolute() / "data"


def solve(path: str):
    data = read_lines(path)


if __name__ == "__main__":
    answer = solve(Path(data_path, "input.txt"))
    print(f"Problem 1: {answer}")