# flake8: noqa: F401
from collections import defaultdict
from pathlib import Path

from solver import utils

data_path = Path(__file__).parent.parent.absolute() / "data"


def solve(path: str):
    data = utils.read_lines(path)

    results = 0
    counter = defaultdict(lambda: {"rocks": 0, "square_index": len(data) + 1})

    for row, line in enumerate(data):
        for col, char in enumerate(line):
            match char:
                case ".":
                    continue

                case "O":
                    counter[col]["rocks"] += 1

                case "#":
                    rocks = counter[col]["rocks"]
                    index = counter[col]["square_index"]

                    for i in range(index - 1, index - rocks - 1, -1):
                        results += i

                    counter[col] = {"rocks": 0, "square_index": len(data) - row}

    for obj in counter.values():
        rocks = obj["rocks"]
        index = obj["square_index"]

        for i in range(index - 1, index - rocks - 1, -1):
            results += i
                    

    return results

            




if __name__ == "__main__":
    answer = solve(Path(data_path, "input.txt"))
    print(f"Problem 1: {answer}")