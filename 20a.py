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

    def within_bounds(i: int, j: int) -> bool:
        return 0 <= i < r and 0 <= j < c

    si, sj, ei, ej = -1, -1, -1, -1

    for i in range(r):
        for j in range(c):
            if inp.grid[i][j] == "S":
                si, sj = i, j
            elif inp.grid[i][j] == "E":
                ei, ej = i, j

    assert si != -1 and ei != -1

    all_dis = {DEF: [[INF for _ in range(c)] for _ in range(r)]}
    q = deque()

    all_dis[DEF][si][sj] = 0
    q.append(((si, sj), DEF))

    while len(q) > 0:
        (ci, cj), cheat = q.popleft()

        if cheat == DEF:  # can still cheat
            for di, dj in DIJ:
                ni, nj, nni, nnj = ci + di, cj + dj, ci + 2 * di, cj + 2 * dj

                if not (
                    within_bounds(nni, nnj)
                    and inp.grid[ni][nj] == "#"
                    and inp.grid[nni][nnj] != "#"
                    and all_dis[DEF][nni][nnj] == INF
                ):
                    continue

                new_cheat = ((ni, nj), (nni, nnj))
                all_dis[new_cheat] = [
                    [all_dis[DEF][i][j] for j in range(c)] for i in range(r)
                ]

                all_dis[new_cheat][nni][nnj] = all_dis[DEF][ci][cj] + 2
                q.append(((nni, nnj), new_cheat))

        for di, dj in DIJ:
            ni, nj = ci + di, cj + dj

            if (
                inp.grid[ni][nj] != "#"
                and all_dis[cheat][ni][nj] > all_dis[cheat][ci][cj] + 1
            ):
                all_dis[cheat][ni][nj] = all_dis[cheat][ci][cj] + 1
                q.append(((ni, nj), cheat))

    ans = 0
    for dis in all_dis.values():
        if all_dis[DEF][ei][ej] - dis[ei][ej] >= 100:
            ans += 1

    return Outp(ans)


def show_output(outp: Outp) -> None:
    print(outp.ans)


def main():
    show_output(solve(get_input()))


main()
