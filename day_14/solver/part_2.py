# flake8: noqa: F401
from collections import defaultdict
from pathlib import Path

from solver import utils

data_path = Path(__file__).parent.parent.absolute() / "data"



def solve(path: str):
    data = utils.read_lines(path)
    data = [list(line) for line in data]

    for line in data:
        index = -1
        count = 0
        print("".join(line))
        for col, char in enumerate(line[:]):
            match char:
                case ".":
                    continue
                case "#":
                    if count == 0:
                        index = col
                        continue

                    new_line = (["O"] * count) + ["."] * ((col - (index + 1)) - count)
        
                    line[index + 1: col] = new_line
                    index = col
                    count = 0
                case "O":
                    count += 1

        print("".join(line))

    results = 0
    return results

            


if __name__ == "__main__":
    answer = solve(Path(data_path, "input.txt"))
    if answer is not None:
        print(f"Problem 2: {answer}")