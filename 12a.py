from dataclasses import dataclass


@dataclass
class Inp:
    grid: list[list[str]]


@dataclass
class Outp:
    ans: int


def get_input() -> Inp:
    with open("in.txt", "r") as f:
        grid = [*map(lambda line: list(line.strip()), f.readlines())]
        return Inp(grid)


def solve(inp: Inp) -> Outp:
    r, c = len(inp.grid), len(inp.grid[0])
    vis = [[False for _ in range(c)] for _ in range(r)]

    def within_bounds(i: int, j: int) -> bool:
        return 0 <= i < r and 0 <= j < c

    results = []

    a, p = 0, 0

    def dfs(i: int, j: int) -> None:
        nonlocal a, p

        a += 1
        vis[i][j] = True

        for d in range(4):
            ni, nj = i + [0, -1, 0, 1][d], j + [1, 0, -1, 0][d]
            if within_bounds(ni, nj):
                if inp.grid[ni][nj] != inp.grid[i][j]:
                    p += 1
                elif not vis[ni][nj]:
                    dfs(ni, nj)
            else:
                p += 1

    for i in range(r):
        for j in range(c):
            if not vis[i][j]:
                a, p = 0, 0
                dfs(i, j)
                results.append((a, p))

    ans = 0
    for a, p in results:
        ans += a * p

    return Outp(ans)


def show_output(outp: Outp) -> None:
    print(outp.ans)


def main():
    show_output(solve(get_input()))


main()
