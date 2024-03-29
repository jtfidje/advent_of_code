from day_04 import run, cleaned


def test_solve_1_run_example():
    assert run.solve_1("example.txt") == 2


def test_solve_2_run_example():
    assert run.solve_2("example.txt") == 4


def test_solve_1_run_input():
    assert run.solve_1("input.txt") == 464


def test_solve_2_run_input():
    assert run.solve_2("input.txt") == 770


def test_solve_1_cleaned_example():
    assert cleaned.solve_1("example.txt") == 2


def test_solve_2_cleaned_example():
    assert cleaned.solve_2("example.txt") == 4


def test_solve_1_cleaned_input():
    assert cleaned.solve_1("input.txt") == 464


def test_solve_2_cleaned_input():
    assert cleaned.solve_2("input.txt") == 770
