# flake8: noqa: F401

from pathlib import Path

from solver import utils

data_path = Path(__file__).parent.parent.absolute() / "data"


def solve(path: str):
    data = utils.read_lines(path)

    for data_i, line in enumerate(data):
        springs, groups = line.split()
        springs = list(springs)
        groups = list(map(int, groups.split(",")))

        start = 0
        for group in groups:
            for i, window in enumerate(utils.sliding_window(springs[start:], window_size=group, step=1), start=start):

                if all(char == "?" for char in window):
                    for j in range(i, i + group):
                        springs[j] = "#"

                    try:
                        if springs[i + group] == "?":
                            springs[i + group] = "."
                    except:
                        ...

                    start = i + group + 1

                    break

        data[data_i] = "".join(springs)

    for line in data:
        print(line)

    return 10

if __name__ == "__main__":
    answer = solve(Path(data_path, "input.txt"))
    print(f"Problem 1: {answer}")