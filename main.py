import argparse
import sys
from dataclasses import dataclass
from typing import List, Set, Tuple

import clingo


@dataclass
class ProblemInput:
    n_queens: int
    rows: int
    cols: int


def read_input() -> ProblemInput:
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="Chess queen domination solver",
        epilog="Example: python3 main.py 2 4 5",
    )
    parser.add_argument("n", type=int, help="number of queens to place")
    parser.add_argument("rows", type=int, help="number of rows on the board")
    parser.add_argument("cols", type=int, help="number of columns on the board")

    args = parser.parse_args()

    errors: List[str] = []
    if args.n < 1:
        errors.append(f"n must be a positive integer, got {args.n}")
    if args.rows < 1:
        errors.append(f"rows must be a positive integer, got {args.rows}")
    if args.cols < 1:
        errors.append(f"cols must be a positive integer, got {args.cols}")

    if errors:
        for error in errors:
            print(f"Error: {error}", file=sys.stderr)
        parser.print_help(sys.stderr)
        sys.exit(1)

    return ProblemInput(n_queens=args.n, rows=args.rows, cols=args.cols)


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


def solve(problem: ProblemInput):
    program = build_asp_program(problem)
    ctl = clingo.Control()
    ctl.add("base", [], program)
    ctl.ground([("base", [])])

    found = False
    with ctl.solve(yield_=True) as handle:
        for model in handle:
            print("Model found:", model)
            found = True

    if not found:
        print(
            f" No solution found for {problem.n_queens} queen(s) on a {problem.rows}×{problem.cols} board."
        )


def main():
    problem = read_input()
    solve(problem)


if __name__ == "__main__":
    main()
