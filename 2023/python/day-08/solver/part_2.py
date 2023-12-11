from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Self

from solver import utils

data_path = Path(__file__).parent.parent.absolute() / "data"

class Node:
    def __init__(self, name: str, left: Self | None, right: Self | None):
        self.name = name
        self.left = left
        self.right = right

    def get_neighbour(self, dir: str) -> Self:
        return self.left if dir == "L" else self.right
    
    def is_terminal(self) -> bool:
        return self.name.endswith("Z")

    def __repr__(self):
        return f"{self.left.name} <-- {self.name} --> {self.right.name}"


def solve(path: str):
    data = utils.read_lines(path)
    
    instructions = data.pop(0)
    data.pop(0)

    node_map = {}
    for line in data:
        name, dirs = line.split(" = ")
        left, right = dirs[1:-1].split(", ")

        node_map[name] = Node(name, None, None)

    for line in data:
        name, dirs = line.split(" = ")
        left, right = dirs[1: -1].split(", ")

        node = node_map[name]
        node.left = node_map[left]
        node.right = node_map[right]
    
    
    
    states = defaultdict(dict)
    for node in node_map.values():
        if not node.name.endswith("A"):
            continue

        cache = {}
        current = node
        counter = 0
        while True:
            i = counter % len(instructions)

            if current.name.endswith("Z"):
                states[node.name]["Z-position"] = {"hit_on": counter}

            c = (current.name, i)
            if c in cache:
                states[node.name]["Loop-position"] = {"first_name": c[0], "first_counter": cache[c], "first_index": c[1], "size": counter - cache[c], "hit_on": counter}
                break
            else:
                cache[c] = counter

            instruction = instructions[i]
            current = current.get_neighbour(instruction)
            counter += 1

    print("State:")
    _states = []
    for key, value in states.items():
        value["name"] = key
        _states.append(value)
    states = sorted(_states, key=lambda x: x["Loop-position"]["size"])
    utils.json_print(states)
    print()


    A = states.pop(0)["Loop-position"]
    B = states.pop(0)["Loop-position"]
    counter = 0
    while states:
        if counter > 0:
            A = states.pop(0)["Loop-position"]
        x = B["size"] % A["size"]

        print(f"{x=}")

        match x:
            case 0:
                total_length = B["size"]

            case 2:
                total_length = B["size"] * 2

            case _:
                total_length = B["size"] * A["size"]

        print(f"{total_length=}")
        print()

        B = {"size": total_length}

        counter += 1

# TOO HIGH: 24085386913221873651759779

if __name__ == "__main__":
    answer = solve(Path(data_path, "input.txt"))
    if answer is not None:
        print(f"Problem 2: {answer}")