# flake8: noqa: F401
from collections import defaultdict
from enum import IntEnum
from typing import Self
from pathlib import Path

from solver import utils

data_path = Path(__file__).parent.parent.absolute() / "data"

results = 0

class Module:
    def __init__(self, name: str, queue: list[tuple[Self, Self, bool]]):
        self.name = name
        self.outputs = []
        self.queue = queue

        self.current_state = False

        self.records = {True: 0, False: 0}

    def add_output(self, module: Self):
        self.outputs.append(module)

    def send(self, pulse: bool):
        for module in self.outputs:
            self.queue.append(
                (
                    self,
                    module,
                    pulse
                )
            )
            self.records[pulse] += 1

    def receive(self, name: str, pulse: bool):
        raise NotImplementedError

class FlipFlop(Module):
    def receive(self, _, pulse: bool):
        if pulse is True:
            return
        
        self.current_state = not self.current_state
        self.send(pulse=self.current_state)

class Conjunction(Module):
    def __init__(self, name: str, queue: list[tuple[Module, Module, bool]]):
        super().__init__(name, queue)
        self.cache = defaultdict(bool)

    def receive(self, name: str, pulse: bool):
        self.cache[name] = pulse

        pulse = not all(self.cache.values())
        self.send(pulse)


class Broadcaster(Module):
    def receive(self, _, pulse: bool):
        self.send(pulse)
        

class Button(Module):
    ...


class Output(Module):
    def receive(self, *args, **kwargs):
        ...


def solve(path: str):
    data = utils.read_lines(path)
    queue: list[tuple[Module, Module, bool]] = []
    modules: dict[str, Module] = {"output": Output("output", None)}
    _outputs: dict[str, list[str]] = {}
    for line in data:
        x, y = line.split(" -> ")

        if x == "broadcaster":
            module = Broadcaster("broadcaster", queue)
        elif x[0] == "%":
            module = FlipFlop(x[1:], queue)
        elif x[0] == "&":
            module = Conjunction(x[1:], queue)

        _outputs[module.name] = y.split(", ")
        modules[module.name] = module

    for key, output_list in _outputs.items():
        module = modules[key]
        for name in output_list:
            module.add_output(modules[name])

    button = Button("button", queue)
    button.add_output(modules["broadcaster"])
    button.send(pulse=False)

    for _ in range(1_000):
        while queue:
            sender, receiver, pulse = queue.pop(0)
            receiver.receive(sender.name, pulse)

    highs, lows = 0, 0
    for module in modules.values():
        highs += module.records[True]
        lows += module.records[False]
    
    return highs * lows


if __name__ == "__main__":
    answer = solve(Path(data_path, "input.txt"))
    print(f"Problem 1: {answer}")