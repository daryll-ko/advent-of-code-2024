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

    ans = 0

    def within_bounds(i: int, j: int) -> bool:
        return 0 <= i < r and 0 <= j < c

    for i in range(r):
        for j in range(c):
            if inp.grid[i][j] != ".":
                continue

            inp.grid[i][j] = "#"

            vis = set([(si, sj, 3)])
            dir = 3
            ci, cj = si, sj

            while True:
                ni, nj = ci + [0, 1, 0, -1][dir], cj + [1, 0, -1, 0][dir]
                #              E  S  W   N

                if not within_bounds(ni, nj):
                    break

                if inp.grid[ni][nj] == "#":
                    dir = (dir + 1) % 4
                else:
                    if (ni, nj, dir) in vis:
                        ans += 1
                        break

                    vis.add((ni, nj, dir))
                    ci, cj = ni, nj

            inp.grid[i][j] = "."

    return Outp(ans)


def show_output(outp: Outp) -> None:
    print(outp.ans)


def main():
    show_output(solve(get_input()))


main()
