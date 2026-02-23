# Chess Queen Domination Solver
## Usage
```sh
echo "<n_queens> <rows> <cols>" | python3 main.py
```
#### Examples:
Input with solution:
```sh
echo "2 4 5" | python3 main.py
```
```
3 2
3 3
```
Input with no solution:
```sh
echo "1 4 4" | python main.py
```
```sh
No solution found for 1 queen(s) on a 4x4 board.
```

## Installation
### Using pip
Prerequisites: Python3, Pip
```sh
pip install clingo
echo "2 4 5" | python3 main.py
```


### Using nix
Prerequisites: [Nix: the package manager](https://nixos.org/download/) with flakes enabled.

```sh
nix develop
echo "2 4 5" | python3 main.py
```
