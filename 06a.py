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

    si, sj = -1, -1

    for i in range(r):
        for j in range(c):
            if inp.grid[i][j] == "^":
                si, sj = i, j

    assert si != -1 and sj != -1

    vis = set([(si, sj)])
    dir = 3
    ci, cj = si, sj

    def within_bounds(i: int, j: int) -> bool:
        return 0 <= i < r and 0 <= j < c

    while True:
        ni, nj = ci + [0, 1, 0, -1][dir], cj + [1, 0, -1, 0][dir]
        #              E  S  W   N

        if not within_bounds(ni, nj):
            break

        if inp.grid[ni][nj] == "#":
            dir = (dir + 1) % 4
        else:
            vis.add((ni, nj))
            ci, cj = ni, nj

    ans = len(vis)

    return Outp(ans)


def show_output(outp: Outp) -> None:
    print(outp.ans)


def main():
    show_output(solve(get_input()))


main()
