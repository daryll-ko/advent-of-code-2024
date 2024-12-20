from collections import deque
from dataclasses import dataclass


@dataclass
class Inp:
    grid: list[list[str]]


@dataclass
class Outp:
    ans: int


DEF = ((-1, -1), (-1, -1))
INF = 10**20
DIJ = [(0, 1), (-1, 0), (0, -1), (1, 0)]


def get_input() -> Inp:
    with open("in.txt", "r") as f:
        grid = [*map(lambda line: list(line.strip()), f.readlines())]
        return Inp(grid)


def solve(inp: Inp) -> Outp:
    r, c = len(inp.grid), len(inp.grid[0])

    si, sj, ei, ej = -1, -1, -1, -1
    free = []

    for i in range(r):
        for j in range(c):
            if inp.grid[i][j] == "S":
                si, sj = i, j
            if inp.grid[i][j] == "E":
                ei, ej = i, j
            if inp.grid[i][j] != "#":
                free.append((i, j))

    assert si != -1 and ei != -1

    all_dis = {
        start: [[INF for _ in range(c)] for _ in range(r)]
        for start in [(si, sj), (ei, ej)]
    }

    for i, j in [(si, sj), (ei, ej)]:
        q = deque()

        all_dis[(i, j)][i][j] = 0
        q.append((i, j))

        while len(q) > 0:
            ci, cj = q.popleft()

            for di, dj in DIJ:
                ni, nj = ci + di, cj + dj

                if (
                    inp.grid[ni][nj] != "#"
                    and all_dis[(i, j)][ni][nj] > all_dis[(i, j)][ci][cj] + 1
                ):
                    all_dis[(i, j)][ni][nj] = all_dis[(i, j)][ci][cj] + 1
                    q.append((ni, nj))

    ans = 0

    for i1, j1 in free:
        for i2, j2 in free:
            if (i1, j1) != (i2, j2) and abs(i1 - i2) + abs(j1 - j2) <= 2:
                optimized = all_dis[(si, sj)][i1][j1] + 2 + all_dis[(ei, ej)][i2][j2]
                if all_dis[(si, sj)][ei][ej] - optimized >= 100:
                    ans += 1

    return Outp(ans)


def show_output(outp: Outp) -> None:
    print(outp.ans)


def main():
    show_output(solve(get_input()))


main()
