# flake8: noqa: F401

from pathlib import Path

from solver import utils

data_path = Path(__file__).parent.parent.absolute() / "data"

def check_mirror(pattern):
    for i in range(len(pattern) - 1):
        j = i + 1

        horizontal_start = i
        is_mirror = False
        while True:
            if pattern[i] != pattern[j]:
                break

            i -= 1
            j += 1


            if i < 0 or j >= len(pattern):
                is_mirror = True
                break

        if is_mirror:
            return horizontal_start + 1


def solve(path: str):
    patterns = utils.read_data(path).split("\n\n")
    patterns = list(map(lambda x: [list(y) for y in x.split()], patterns))

    horizontal_res = 0
    vertical_res = 0
    for pattern in patterns:
        for row, line in enumerate(pattern):
            for col, char in enumerate(line):
                _temp = char

                line[col] = "." if char == "#" else "#"
                res_1 = check_mirror(pattern)

                # check columns
                _pattern = []
                for i in range(len(pattern[0])):
                    column = [row[i] for row in pattern]
                    _pattern.append(column)

                res_2 = check_mirror(_pattern)

                if res_1 is None or res_2 is None:
                    line[col] = _temp
                    continue

                horizontal_res += res_1
                vertical_res += res_2
                break
            else:
                continue

            break
        else:
            continue
        break

    return vertical_res + (horizontal_res * 100)


if __name__ == "__main__":
    answer = solve(Path(data_path, "input.txt"))
    if answer is not None:
        print(f"Problem 2: {answer}")