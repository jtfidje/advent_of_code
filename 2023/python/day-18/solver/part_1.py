import re
# flake8: noqa: F401

from pathlib import Path

from solver import utils

data_path = Path(__file__).parent.parent.absolute() / "data"


def solve(path: str):
    data = utils.read_lines(path)
    data = [line.split(" (")[0] for line in data]

    pos = (0,0)
    points = []
    min_col = 0
    min_row = 0
    max_col = 0
    max_row = 0
    for line in data:
        direction, number = line.split()
        number = int(number)

        match direction:
            case "R":
                for _ in range(number):
                    pos = (
                        pos[0], 
                        pos[1] + 1
                    )
                    points.append(pos)

                    max_col = max(max_col, pos[1])
                    
            case "L":
                for _ in range(number):
                    pos = (
                        pos[0], 
                        pos[1] - 1
                    )
                    points.append(pos)

                    min_col = min(min_col, pos[1])

            case "U":
                for _ in range(number):
                    pos = (
                        pos[0] - 1, 
                        pos[1]
                    )
                    points.append(pos)

                    min_row = min(min_row, pos[0])

            case "D":
                for _ in range(number):
                    pos = (
                        pos[0] + 1, 
                        pos[1]
                    )
                    points.append(pos)

                    max_row = max(max_row, pos[0])

    matrix = []
    for _ in range(max_row + abs(min_row) + 1):
        line = ["."] * (max_col + abs(min_col) + 1)
        matrix.append(line)

    for point in points:
        row = point[0] + abs(min_row)
        col = point[1] + abs(min_col)

        matrix[row][col] = "#"

    
    with open("/tmp/res.txt", "w") as f:
        for line in matrix:
            f.write("".join(line) + "\n")


    pattern = r"(?:(\.*#+)(\.*)(#+\.*))"

    for i, line in enumerate(matrix):
        temp = line[:]
        line = "".join(line)
        for match in re.finditer(pattern, line):
            group = match.groups()[1]
            res = re.sub(pattern, r"\1" + "#" * len(group) + r"\3", line[match.start():match.end()], count=1)

            temp[match.start():match.end()] = list(res)
            
        matrix[i] = "".join(temp)

    

    return "".join(matrix).count("#")




if __name__ == "__main__":
    answer = solve(Path(data_path, "input.txt"))
    #answer = solve(Path(data_path, "example_1.txt"))
    print(f"Problem 1: {answer}")