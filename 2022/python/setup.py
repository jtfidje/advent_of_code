import argparse
import os
import pathlib
import re
import requests
import subprocess
import time
from datetime import datetime

_year, _today = datetime.now().strftime("%Y,%d").split(",")

parser = argparse.ArgumentParser()
parser.add_argument(
    "year",
    type=str,
    help="AoC year (i.e.: 2022)",
    nargs="?",
    default=_year
)

parser.add_argument(
    "day",
    type=str,
    help="AoC Day as string (i.e.: 02)",
    nargs="?",
    default=_today
)
args = parser.parse_args()

year = args.year
day = args.day

aoc_base_url = f"https://adventofcode.com/{year}/day/{int(day)}"
aoc_input_url = f"{aoc_base_url}/input"
project_path = f"{pathlib.Path(__file__).parent.absolute()}/day_{day}"


subprocess.run(["poetry", "new", "--readme", "rst", f"day_{day}"])
os.chdir(project_path)
subprocess.run(["poetry", "add", "--group", "dev", "pytest"])
subprocess.run(["touch", "example.txt", f"day_{day}/cleaned.py"])


print("Getting input from:", aoc_input_url)
sess = requests.Session()
sess.cookies.set("session", os.environ.get("AOC_SESSION"))

# Fetch title
res = sess.get(aoc_base_url)
res.raise_for_status()
title_banner = re.search(r"(--- Day \d+: .* ---)", res.text)[1]

time.sleep(0.5)

# Fetch input
res = sess.get(aoc_input_url)
res.raise_for_status()

project_input_path = f"{project_path}/input.txt"
print("Writing input to:", project_input_path)
with open(project_input_path, "w") as f:
    f.write(res.text)

project_tests_path = f"{project_path}/tests/test_day_{day}.py"
print("Writing test templates into:", project_tests_path)
test_template = f"""
from day_{day} import run, cleaned


def test_solve_1_run_example():
    assert run.solve_1("example.txt") == None


def test_solve_2_run_example():
    assert run.solve_2("example.txt") == None


#def test_solve_1_run_input():
#    assert run.solve_1("input.txt") == None
#
#
#def test_solve_2_run_input():
#    assert run.solve_2("input.txt") == None
#
#
#def test_solve_1_cleaned_example():
#    assert cleaned.solve_1("example.txt") == None
#
#
#def test_solve_2_cleaned_example():
#    assert cleaned.solve_2("example.txt") == None
#
#
#def test_solve_1_cleaned_input():
#    assert cleaned.solve_1("input.txt") == None
#
#
#def test_solve_2_cleaned_input():
#    assert cleaned.solve_2("input.txt") == None
"""[1:]
with open(project_tests_path, "w") as f:
    f.write(test_template)

project_run_path = f"{project_path}/day_{day}/run.py"
print("Writing run templates into:", project_run_path)
run_template = """
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


def read_numbers(path: str) -> list[int]:
    with open(path, "r") as f:
        lines = [line for line in f.readlines()]
        lines = [line.strip() for line in lines]
        return list(map(int, lines))


def solve_1(path: str) -> Any:
    data = read_lines(path)
    ...


def solve_2(path: str) -> Any:
    data = read_lines(path)
    ...


if __name__ == "__main__":
    print(f"Example 1: {solve_1('example.txt')}")
    print(f"Example 2: {solve_2('example.txt')}")
    print("\\n- - -\\n")
    print(f"Problem 1: {solve_1('input.txt')}")
    print(f"Problem 2: {solve_2('input.txt')}")
"""[1:]  # noqa: W291, W293
with open(project_run_path, "w") as f:
    f.write(run_template)

project_readme_path = f"{project_path}/README.rst"
print("Writing README template into:", project_readme_path)
readme_template = f"""
**************************
{title_banner}
**************************
`<https://adventofcode.com/2022/day/{day}>`_


Personal Stats:
###############


========  ====  =====  ========  ====  =====
Part 1                 Part 2       
---------------------  ---------------------
Time      Rank  Score  Time      Rank  Score
========  ====  =====  ========  ====  =====

========  ====  =====  ========  ====  =====
"""  # noqa: W291
with open(project_readme_path, "w") as f:
    f.write(readme_template)

# Starting watchdog!
try:
    subprocess.run(
        (
            f"while inotifywait -re modify {project_path} ;"
            "do poetry run pytest tests/ "
            f"&& poetry run python {project_path}/day_{day}/run.py;"
            "done"
        ),
        shell=True
    )
except KeyboardInterrupt:
    ...
