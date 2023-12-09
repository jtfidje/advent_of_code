from __future__ import annotations

import multiprocessing
import time
from enum import StrEnum
from pathlib import Path
from typing import Self

from solver import utils

data_path = Path(__file__).parent.parent.absolute() / "data"


class WorkerState(StrEnum):
    pending = "pending"
    running = "running"
    halted = "halted"
    finished = "finished"


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
        return f"{self.left} <-- {self.name} --> {self.right}"


def work(
        worker_id: str,
        node: Node,
        instructions: str,
        to_manager_queue: multiprocessing.Queue,
        from_manager_queue: multiprocessing.Queue):
    print(worker_id, "started!")
    current_state = WorkerState.running
    index = 0
    while True:
        if current_state == WorkerState.halted:
            continue

        if node.is_terminal():
            to_manager_queue.put(index)
            
            new_state = from_manager_queue.get()
            if new_state == WorkerState.finished:
                break

        i = index % len(instructions)
        instruction = instructions[i]
        node = node.get_neighbour(instruction)

        index += 1


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

    nodes = [node for node in node_map.values() if node.name.endswith("A")]
    with multiprocessing.Manager() as manager:
        workers: list[dict] = []
        for i, node in enumerate(nodes):
            to_manager_queue = manager.Queue()
            from_manager_queue = manager.Queue()
            worker_id = f"Worker-{i}"
        
            process = multiprocessing.Process(
                target=work,
                args=(worker_id, node, instructions, to_manager_queue, from_manager_queue)
            )

            workers.append({
                "name": worker_id,
                "to_manager_queue": to_manager_queue,
                "from_manager_queue": from_manager_queue,
                "process": process
            })
            process.start()

        index = None
        print("Main process entering loop...")
        while True:
            indices = set()
            for worker in workers:
                index = worker["to_manager_queue"].get()
                indices.add(index)

            if len(indices) == 1:
                for worker in workers:
                    worker["from_manager_queue"].put(WorkerState.finished)
                    worker["process"].join()
                index = indices[0]
                break
            
            for worker in workers:
                worker["from_manager_queue"].put(WorkerState.running)
    
    return index


if __name__ == "__main__":
    answer = solve(Path(data_path, "input.txt"))
    if answer is not None:
        print(f"Problem 2: {answer}")