from dataclasses import dataclass


@dataclass
class Inp:
    grid: list[list[int]]


@dataclass
class Outp:
    total_score: int


def get_input() -> Inp:
    with open("in.txt", "r") as f:
        grid = [*map(lambda line: [*map(int, list(line.strip()))], f.readlines())]
        return Inp(grid)


def solve(inp: Inp) -> Outp:
    r, c = len(inp.grid), len(inp.grid[0])

    def within_bounds(i: int, j: int) -> bool:
        return 0 <= i < r and 0 <= j < c

    total_score = 0

    def dfs(i: int, j: int) -> None:
        nonlocal total_score

        if inp.grid[i][j] == 9:
            total_score += 1
            return

        for d in range(4):
            ni, nj = i + [0, -1, 0, 1][d], j + [1, 0, -1, 0][d]
            if within_bounds(ni, nj) and inp.grid[ni][nj] == inp.grid[i][j] + 1:
                dfs(ni, nj)

    for i in range(r):
        for j in range(c):
            if inp.grid[i][j] == 0:
                dfs(i, j)

    return Outp(total_score)


def show_output(outp: Outp) -> None:
    print(outp.total_score)


def main():
    show_output(solve(get_input()))


main()
