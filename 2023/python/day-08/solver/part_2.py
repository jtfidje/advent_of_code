# flake8: noqa: F401

from pathlib import Path

from solver import utils

data_path = Path(__file__).parent.parent.absolute() / "data"


class Node:
    def __init__(self, name: str, left: str, right: str):
        self.name = name
        self.left = left
        self.right = right

    def get_neighbour(self, dir: str):
        return self.left if dir == "L" else self.right
    
    def is_terminal(self) -> bool:
        return self.name.endswith("Z")

    def __repr__(self):
        return f"{self.left} <-- {self.name} --> {self.right}"

def solve(path: str):
    data = utils.read_lines(path)
    
    instructions = data.pop(0)
    data.pop(0)

    node_map = {}
    for line in data:
        name, dirs = line.split(" = ")
        left, right = dirs[1:-1].split(", ")

        node_map[name] = Node(name, left, right)

    nodes = [node for node in node_map.values() if node.name.endswith("A")]
    counter = 0
    while True:
        i = counter % len(instructions)
        instruction = instructions[i]
        
        counter += 1

        for _ in range(len(nodes)):
            node = nodes.pop(0)
            nodes.append(node_map[node.get_neighbour(instruction)])

        if all(node.is_terminal() for node in nodes):
            break
    
    return counter


if __name__ == "__main__":
    answer = solve(Path(data_path, "input.txt"))
    if answer is not None:
        print(f"Problem 2: {answer}")