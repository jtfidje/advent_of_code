# flake8: noqa: F401
from collections import defaultdict
from pathlib import Path

from solver import utils

data_path = Path(__file__).parent.parent.absolute() / "data"


def solve(path: str):
    data = utils.read_lines(path)

    counter = defaultdict(lambda: defaultdict(lambda: {"rocks": 0, "row": len(data) + 1}))
    current_square = defaultdict(int)
    for row, line in enumerate(data):
        for col, char in enumerate(line):
            match char:
                case ".":
                    continue

                case "#":
                    current_square[col] += 1
                    counter[col][current_square[col]]["row"] = row
                    continue

                case "O":
                    square = current_square[col]
                    counter[col][square]["rocks"] += 1

    results = 0
    for col, element in counter.items():
        for _element in element.values():
            if _element["rocks"] == 0:
                continue

            rock_count = _element["rocks"]
            square_index = _element["row"]

            print(col, rock_count, square_index)

            for i in range(square_index - 1, square_index - rock_count, - 1):
                print(i)
                
                results += i

            print()

    return results

            




if __name__ == "__main__":
    answer = solve(Path(data_path, "input.txt"))
    print(f"Problem 1: {answer}")