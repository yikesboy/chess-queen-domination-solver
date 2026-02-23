import sys
from dataclasses import dataclass
from typing import List, Tuple

import clingo


@dataclass
class ProblemInput:
    n_queens: int
    rows: int
    cols: int


def read_input() -> ProblemInput:
    line = sys.stdin.read().strip()
    parts = line.split()
    if len(parts) != 3:
        print("Usage: exptected 3 space separated integers <n> <rows> <cols>")
        sys.exit(1)

    try:
        n, rows, cols = int(parts[0]), int(parts[1]), int(parts[2])
    except ValueError:
        print("Error: all inputs must be integers")
        sys.exit(1)

    if n < 1:
        print(f"n must be a positive integer, got {n}")
        sys.exit(1)
    if rows < 1:
        print(f"rows must be a positive integer, got {rows}")
        sys.exit(1)
    if cols < 1:
        print(f"cols must be a positive integer, got {cols}")
        sys.exit(1)

    return ProblemInput(n_queens=n, rows=rows, cols=cols)


def build_asp_program(problem: ProblemInput) -> str:
    return f"""
    rows(1..{problem.rows}).
    cols(1..{problem.cols}).
    n_queens({problem.n_queens}).

    {{ queen(C, R) : cols(C), rows(R) }}.

    :- n_queens(N), #count {{ C, R : queen(C, R) }} != N.

    dominated(C, R) :- queen(C, R).
    dominated(C, R) :- queen(C2, R), cols(C), cols(C2).
    dominated(C, R) :- queen(C, R2), rows(R), rows(R2).
    dominated(C, R) :- queen(C2, R2), cols(C), rows(R), C - C2 == R - R2.
    dominated(C, R) :- queen(C2, R2), cols(C), rows(R), C - C2 == R2 - R.

    :- cols(C), rows(R), not dominated(C, R).
    """

def parse_output(model: clingo.Model) -> List[Tuple[int, int]]:
    queens: List[Tuple[int, int]] = []
    for atom in model.symbols(shown=True):
        if atom.name == "queen" and len(atom.arguments) == 2:
            col = atom.arguments[0].number
            row = atom.arguments[1].number
            queens.append((col, row))
    return queens

def solve(problem: ProblemInput):
    program = build_asp_program(problem)
    ctl = clingo.Control(["--models=1"])
    ctl.add("base", [], program)
    ctl.ground([("base", [])])

    found = False
    with ctl.solve(yield_=True) as handle:
        for model in handle:
            found = True
            for col, row in parse_output(model):
                print(f"{col} {row}")
    if not found:
        print(f"No solution found for {problem.n_queens} queen(s) on a {problem.rows}x{problem.cols} board.")

def main():
    problem = read_input()
    solve(problem)


if __name__ == "__main__":
    main()
