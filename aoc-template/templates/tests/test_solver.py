from pathlib import Path

from solver import run

data_path = Path(__file__).parent.parent.absolute() / "data"


def test_solve_1_run_example():
    assert run.solve_1(data_path / "example_1.txt") == None


def test_solve_2_run_example():
    assert run.solve_2(data_path / "example_2.txt") == None


# def test_solve_1_run_input():
#    assert run.solve_1(data_path / "input.txt") == None
#
#
# def test_solve_2_run_input():
#    assert run.solve_2(data_path / "input.txt") == None
#
#
# def test_solve_1_cleaned_example():
#    assert cleaned.solve_1(data_path / "example.txt") == None
#
#
# def test_solve_2_cleaned_example():
#    assert cleaned.solve_2(data_path / "example.txt") == None
#
#
# def test_solve_1_cleaned_input():
#    assert cleaned.solve_1(data_path / "input.txt") == None
#
#
# def test_solve_2_cleaned_input():
#    assert cleaned.solve_2(data_path / "input.txt") == None
