import math
import re
from functools import cache
from pathlib import Path

from solver import utils

data_path = Path(__file__).parent.parent.absolute() / "data"


maps = {}


@cache
def get_location(seed):
    next_index = seed
    for _map in maps.values():
        for (dest, start, r) in _map:
            _range = range(start, start + r)
            if next_index in _range:
                _index = _range.index(next_index)
                next_index = range(dest, dest + r)[_index]
                break
    return next_index

def solve(path: str):
    data = utils.read_data(path)
    data = re.sub(r"[\n]{2,}", "\n", data)
    seeds = list(map(int, re.search(r"seeds:\s((?:\d+\s)+)", data).groups()[0].split()))
    
    maps["seed_to_soil"] = [list(map(int, line.split())) for line in re.search(r"seed-to-soil map:\s((?:\d+\s)+)", data).groups()[0].split("\n") if line]
    maps["soil_to_fertilizer"] = [list(map(int, line.split())) for line in re.search(r"soil-to-fertilizer map:\s((?:\d+\s)+)", data).groups()[0].split("\n") if line]
    maps["fertilizer_to_water"] = [list(map(int, line.split())) for line in re.search(r"fertilizer-to-water map:\s((?:\d+\s)+)", data).groups()[0].split("\n") if line]
    maps["water_to_light"] = [list(map(int, line.split())) for line in re.search(r"water-to-light map:\s((?:\d+\s)+)", data).groups()[0].split("\n") if line]
    maps["light_to_temp"] = [list(map(int, line.split())) for line in re.search(r"light-to-temperature map:\s((?:\d+\s)+)", data).groups()[0].split("\n") if line]
    maps["temp_to_humidity"] = [list(map(int, line.split())) for line in re.search(r"temperature-to-humidity map:\s((?:\d+\s)+)", data).groups()[0].split("\n") if line]
    maps["humidity_to_location"] = [list(map(int, line.split())) for line in re.search(r"humidity-to-location map:\s((?:\d+\s*)+)", data).groups()[0].split("\n") if line]

    min_loc = math.inf
    # Find max seed
    for _start, _len in utils.sliding_window(array=seeds, window=2, step=2):
        for element in range(_start, _start + _len):
            loc = get_location(seed=element)

            min_loc = min(min_loc, loc)


    return min_loc



if __name__ == "__main__":
    answer = solve(Path(data_path, "input.txt"))
    print(f"Problem 1: {answer}")