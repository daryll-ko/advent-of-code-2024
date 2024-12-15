from collections import defaultdict
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

    ants = defaultdict(list)
    for i in range(r):
        for j in range(c):
            if (kind := inp.grid[i][j]) != ".":
                ants[kind].append((i, j))

    def within_bounds(i: int, j: int) -> bool:
        return 0 <= i < r and 0 <= j < c

    anti = set()
    for vs in ants.values():
        m = len(vs)
        for ii in range(m):
            for jj in range(ii + 1, m):
                i1, j1 = vs[ii]
                i2, j2 = vs[jj]

                i3, j3 = i1 - (i2 - i1), j1 - (j2 - j1)
                i4, j4 = i2 + (i2 - i1), j2 + (j2 - j1)

                if within_bounds(i3, j3):
                    anti.add((i3, j3))

                if within_bounds(i4, j4):
                    anti.add((i4, j4))

    return Outp(len(anti))


def show_output(outp: Outp) -> None:
    print(outp.ans)


def main():
    show_output(solve(get_input()))


main()