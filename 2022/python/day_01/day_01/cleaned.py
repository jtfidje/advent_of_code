from functools import reduce


def read_data(path: str) -> list[list[int]]:
    with open(path, "r") as f:
        data = f.read().strip().split("\n\n")
    data = list(map(lambda x: x.split("\n"), data))
    data = list(map(lambda x: list(map(int, x)), data))
    return data


def solve_1(data: list[list[int]]) -> int:
    return reduce(max, map(sum, data))


def solve_2(data: list[list[int]]) -> int:
    data = sorted(map(sum, data))
    return sum(data[-3:])


if __name__ == "__main__":
    example_data = read_data("example.txt")
    input_data = read_data("input.txt")

    print(f"Example 1: {solve_1(example_data)}")
    print(f"Example 2: {solve_2(example_data)}")
    print("\n- - -\n")
    print(f"Problem 1: {solve_1(input_data)}")
    print(f"Problem 2: {solve_2(input_data)}")