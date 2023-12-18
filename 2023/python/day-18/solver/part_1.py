import re
# flake8: noqa: F401

from pathlib import Path

from solver import utils

data_path = Path(__file__).parent.parent.absolute() / "data"


def solve(path: str):
    data = utils.read_lines(path)
    data = [line.split(" (")[0] for line in data]

    max_width = 0
    max_height = 0
    height = 0
    width = 0
    for line in data:
        direction, number = line.split()
        number = int(number)

        if direction == "R":
            width += number
            max_width = max(max_width, width)
        elif direction == "L":
            width -= number
        elif direction == "U":
            height -= number
        elif direction == "D":
            height += number
            max_height = max(max_height, height)

    matrix = []
    for _ in range(max_height + 1):
        line = ["."] * (max_width + 1)
        matrix.append(line)

    position = [0,0]
    matrix[0][0] = "#"
    for line in data:
        direction, number = line.split()
        number = int(number)

        try:
            match direction:
                case "R":
                    for _ in range(number):
                        position[1] += 1
                        matrix[position[0]][position[1]] = "#"
                
                case "L":
                    for _ in range(number):
                        position[1] -= 1
                        matrix[position[0]][position[1]] = "#"

                case "U":
                    for _ in range(number):
                        position[0] -= 1
                        matrix[position[0]][position[1]] = "#"

                case "D":
                    for _ in range(number):
                        position[0] += 1
                        matrix[position[0]][position[1]] = "#"
        except:
            breakpoint()

    pattern = r"(^\.*#+)(\.*)(#+\.*$)"
    for i, line in enumerate(matrix):
        line = "".join(line)
        match = re.search(pattern, line)
        if match is None:
            continue
        group = match.groups()[1]

        res = re.sub(pattern, r"\1" + "#" * len(group) + r"\3", line)
        matrix[i] = res

    return "".join(matrix).count("#")




if __name__ == "__main__":
    answer = solve(Path(data_path, "input.txt"))
    print(f"Problem 1: {answer}")