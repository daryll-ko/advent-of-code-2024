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


DI = [0, -1, 0, 1]
DJ = [1, 0, -1, 0]


def solve(inp: Inp) -> Outp:
    r, c = len(inp.grid), len(inp.grid[0])
    vis = [[False for _ in range(c)] for _ in range(r)]

    def within_bounds(i: int, j: int) -> bool:
        return 0 <= i < r and 0 <= j < c

    results = []

    a, s = 0, 0

    def dfs(i: int, j: int) -> None:
        nonlocal a, s

        a += 1
        vis[i][j] = True

        for d in range(4):
            ni, nj = i + DI[d], j + DJ[d]
            if within_bounds(ni, nj):
                if inp.grid[ni][nj] != inp.grid[i][j]:

                    for dd in [1, -1]:
                        ni2, nj2 = i + DI[(d + dd) % 4], j + DJ[(d + dd) % 4]
                        if (
                            not within_bounds(ni2, nj2)
                            or inp.grid[ni2][nj2] != inp.grid[i][j]
                        ):
                            s += 1
                        else:
                            nni, nnj = ni2 + DI[d], nj2 + DJ[d]
                            if (
                                within_bounds(nni, nnj)
                                and inp.grid[nni][nnj] == inp.grid[i][j]
                            ):
                                s += 1

                elif not vis[ni][nj]:
                    dfs(ni, nj)
            else:
                for dd in [1, -1]:
                    ni2, nj2 = i + DI[(d + dd) % 4], j + DJ[(d + dd) % 4]
                    if (
                        not within_bounds(ni2, nj2)
                        or inp.grid[ni2][nj2] != inp.grid[i][j]
                    ):
                        s += 1
                    else:
                        nni, nnj = ni2 + DI[d], nj2 + DJ[d]
                        if (
                            within_bounds(nni, nnj)
                            and inp.grid[nni][nnj] == inp.grid[i][j]
                        ):
                            s += 1

    for i in range(r):
        for j in range(c):
            if not vis[i][j]:
                a, s = 0, 0
                dfs(i, j)
                results.append((a, s))

    ans = 0
    for a, s in results:
        ans += a * s
    ans //= 2  # sides were double-counted

    return Outp(ans)


def show_output(outp: Outp) -> None:
    print(outp.ans)


def main():
    show_output(solve(get_input()))


main()
