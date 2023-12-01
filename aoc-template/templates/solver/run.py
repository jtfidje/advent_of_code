# flake8: noqa: F841

import json
from functools import reduce  # noqa: F401
from pathlib import Path
from typing import Any, Generator

data_path = Path(__file__).parent.parent.absolute() / "data"


def json_print(obj: dict | list) -> None:
    print(json.dumps(obj, indent=4))


def read_lines(path: str) -> list[str]:
    with open(path, "r") as f:
        lines = [line for line in f.readlines()]
        lines = [line.strip() for line in lines]
        return lines


def read_numbers(path: str) -> list[int]:
    with open(path, "r") as f:
        lines = [line for line in f.readlines()]
        lines = [line.strip() for line in lines]
        return list(map(int, lines))


def sliding_window(
    array: list, window: int, step: int | None = None
) -> Generator[list, None, None]:
    if step is None:
        step = window
    for i in range(0, len(array) - window + 1, step):
        yield array[i : i + window]


def solve_1(path: str) -> Any:
    data = read_lines(path)
    ...


def solve_2(path: str) -> Any:
    data = read_lines(path)
    ...


if __name__ == "__main__":
    example_1 = solve_1(Path(data_path, "example_1.txt"))
    if example_1 is not None:
        print(f"Example 1: {example_1}")

    example_2 = solve_2(Path(data_path, "example_2.txt"))
    if example_2 is not None:
        print(f"Example 2: {example_2}")

    print("\n- - -\n")

    problem_1 = solve_1(Path(data_path, "input.txt"))
    if problem_1 is not None:
        print(f"Problem 1: {problem_1}")

    problem_2 = solve_2(Path(data_path, "input.txt"))
    if problem_2 is not None:
        print(f"Problem 2: {problem_2}")
