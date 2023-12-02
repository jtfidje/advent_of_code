import argparse
import os
import re
import subprocess
import sys
import time
from contextlib import contextmanager
from datetime import datetime
from zoneinfo import ZoneInfo

from loguru import logger
from requests import Session
from rich import print

from aoc_template.config import settings


def block_execution(year: int, day: int):
    """Block execution until the time has passed a target time
    
    Target: {year}-12-{day}T06:00:00 Europe/Oslo
    """
    target_time = datetime(year, 12, day, 6, 0, 0, tzinfo=ZoneInfo("Europe/Oslo"))
    
    _now = None
    def puzzle_released() -> bool:
        nonlocal _now
        _now = datetime.now(tz=ZoneInfo("Europe/Oslo"))
        return _now >= target_time

    if puzzle_released():
        return
    
    msg_template = f"  Waiting for puzzle to be released @ {target_time.strftime('%d.%b %H:%M:%S')} ... "
    while not puzzle_released():
        print(f"[bold][grey74]{msg_template}[/grey74][grey46]{_now.strftime('%d.%b %H:%M:%S')}[/grey46][/bold]", end="\r")
        time.sleep(0.5)
    print()



def parse_arguments() -> tuple[str, str]:
    """Parse input arguments to get puzzle year and day

    Defaults to today's year and day

    Returns:
        tuple[str, str]: Returns the year and day to use
    """
    _year, _today = datetime.now().strftime("%Y %d").split()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "year", type=str, help="AoC year (i.e.: 2022)", nargs="?", default=_year
    )

    parser.add_argument(
        "day", type=str, help="AoC Day as string (i.e.: 02)", nargs="?", default=_today
    )
    args = parser.parse_args()

    return args.year, args.day


@contextmanager
def get_aoc_session() -> Session:
    """Returns a requests.Session with the AoC session cookie set

    Returns:
        Session: The requests.Session with the AoC session cookie set
    """
    session = Session()
    session.cookies.set("session", settings.aoc_session)

    try:
        yield session
    finally:
        session.close()


def fetch_puzzle_input(puzzle_url: str, session: Session) -> str:
    """Fetches the puzzle input from the AoC website

    Args:
        puzzle_url (str): Puzzle URL to fetch the input for
        session (Session): The requests.Session to use for the request

    Returns:
        str: The puzzle input as a string
    """
    try:
        response = session.get(f"{puzzle_url}/input")
        response.raise_for_status()
    except Exception as err:
        logger.error(f"Failed to fetch puzzle input: {err}")
        sys.exit(1)

    return response.text


def fetch_puzzle_title(puzzle_url: str, session: Session) -> str:
    """Fetches the puzzle title from the AoC website

    Args:
        puzzle_url (str): Puzzle URL to fetch the title for
        session (Session): The requests.Session to use for the request

    Returns:
        str: The puzzle title as a string
    """
    try:
        response = session.get(f"{puzzle_url}")
        response.raise_for_status()
    except Exception as err:
        logger.error(f"Failed to fetch puzzle title: {err}")
        sys.exit(1)

    return re.search(r"(--- Day \d+: .* ---)", response.text)[1]


def start_vscode(project_path: str):
    """Starts VSCode in the project path and open relevant files

    Args:
        project_path (str): The path to the project to open
    """
    try:
        subprocess.run(
            (
                f"code-insiders --reuse-window "
                f"{project_path} "
                f"{project_path}/data/example_1.txt "
                f"{project_path}/data/example_2.txt "
                f"{project_path}/tests/test_solver.py "
                f"{project_path}/solver/part_1.py "
                f"{project_path}/solver/part_2.py "
                f"{project_path}/solver/utils.py "
                f"{project_path}/data/input.txt"
            ),
            shell=True,
        )
    except Exception as err:
        logger.error(f"Failed to start VSCode: {err}")
        sys.exit(1)


def start_watcher(project_path: str):
    """Starts an inotifywait-watcher that performs the following on change:

      - clear the screen
      - run all tests
      - run the solvers

    Args:
        project_path (str): The path to the project to watch
    """
    os.chdir(project_path)
    subprocess.run(
        (
            "PYTHONDONOTWRITEBYTECODE=1 bash -c '"
            f"while inotifywait -q -re modify {project_path} ; "
            "do clear && "
            "poetry run pytest tests/ -p no:cacheprovider && "
            "poetry run python solver/part_1.py && "
            "poetry run python solver/part_2.py ; "
            "done'"
        ),
        shell=True,
    )