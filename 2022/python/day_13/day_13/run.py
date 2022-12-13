import json
from functools import reduce
from typing import Any

def json_print(obj: dict | list) -> None:
    print(json.dumps(obj, indent=4))


def read_lines(path: str) -> list[str]:
    with open(path, "r") as f:
        lines = [line for line in f.readlines()]
        lines = [line.strip() for line in lines]
        return lines


def read_data(path: str) -> list[str]:
    pairs = []
    with open(path, "r") as f:
        data = f.read().strip()
        data = data.split("\n\n")
        for pair in data:
            pair = pair.strip().split("\n")
            pairs.append([
                json.loads(pair[0]),
                json.loads(pair[1])
            ])

        return pairs


def read_numbers(path: str) -> list[int]:
    with open(path, "r") as f:
        lines = [line for line in f.readlines()]
        lines = [line.strip() for line in lines]
        return list(map(int, lines))


def compare(left, right):
    print(left)
    print(right)
    print("-")
    while True:
        if left == [] and right == []:
            return None
        try:
            l = left.pop(0)
        except IndexError:
            return True

        try:
            r = right.pop(0)
        except IndexError:
            return False
        
        if all([isinstance(l, int), isinstance(r, int)]):
            if l > r:
                return False

            elif l < r:
                return True
            
            else: 
                continue
        
        elif all([isinstance(l, list), isinstance(r, list)]):
            res = compare(l, r)
            if res is None:
                continue
            return res
        
        else:
            if isinstance(l, int):
                l = [l]
            else:
                r = [r]
            
            res = compare(l, r)
            if res is None:
                continue
            return res


def solve_1(path: str) -> Any:
    pairs = read_data(path)
    indices = []
    for i, (left, right) in enumerate(pairs, start=1):

        if compare(left, right):
            print("True")
            indices.append(i)
        else:
            print("False")
        print()

    return sum(indices)
                


def solve_2(path: str) -> Any:
    data = read_lines(path)
    ...


if __name__ == "__main__":
    print(f"Example 1: {solve_1('example.txt')}")
    print(f"Example 2: {solve_2('example.txt')}")
    print("\n- - -\n")
    print(f"Problem 1: {solve_1('input.txt')}")
    print(f"Problem 2: {solve_2('input.txt')}")
