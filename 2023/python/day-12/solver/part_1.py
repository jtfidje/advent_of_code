import re

from pathlib import Path

from solver import utils

data_path = Path(__file__).parent.parent.absolute() / "data"


def recursive_check(string: str, pattern: str):
    if "?" not in string:
        match = re.match(pattern, string) is not None
        return 1 if match else 0

    res = 0

    res += recursive_check(string.replace("?", ".", 1), pattern)
    res += recursive_check(string.replace("?", "#", 1), pattern)

    return res


def solve(path: str):
    data = utils.read_lines(path)

    results = 0
    for line in data:
        springs, groups = line.split()
        groups = list(map(int, groups.split(",")))

        pattern = r"^\.*#" + r"\.+#".join("{" + str(group) + "}" for group in groups) + r"\.*$"
        
        results += recursive_check(springs, pattern)

    return results

if __name__ == "__main__":
    answer = solve(Path(data_path, "input.txt"))
    print(f"Problem 1: {answer}")