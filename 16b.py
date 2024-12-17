from collections import defaultdict
from dataclasses import dataclass

import heapq


@dataclass
class Inp:
    grid: list[list[str]]


@dataclass
class Outp:
    ans: int


INF = 10**20
DI = [0, -1, 0, 1]
DJ = [1, 0, -1, 0]


def get_input() -> Inp:
    with open("in.txt", "r") as f:
        grid = [*map(lambda line: list(line.strip()), f.readlines())]

        return Inp(grid)


# bet 393 and 461
def solve(inp: Inp) -> Outp:
    r, c = len(inp.grid), len(inp.grid[0])

    si, sj, ei, ej = -1, -1, -1, -1

    for i in range(r):
        for j in range(c):
            if inp.grid[i][j] == "S":
                si, sj = i, j
            elif inp.grid[i][j] == "E":
                ei, ej = i, j

    assert si != -1 and ei != -1

    pq = []
    heapq.heapify(pq)
    best = [[[INF for _ in range(4)] for _ in range(c)] for _ in range(r)]

    heapq.heappush(pq, (0, (si, sj, 0)))
    best[si][sj][0] = 0

    best_graph = defaultdict(list)

    while len(pq) > 0:
        w, (ci, cj, d) = heapq.heappop(pq)

        if ci == ei and cj == ej:
            continue

        ni, nj = ci + DI[d], cj + DJ[d]

        if inp.grid[ni][nj] != "#" and best[ni][nj][d] >= w + 1:
            best[ni][nj][d] = w + 1
            heapq.heappush(pq, (w + 1, (ni, nj, d)))
            best_graph[(ci, cj, d)].append(0)

        if best[ci][cj][(d + 1) % 4] >= w + 10**3:
            best[ci][cj][(d + 1) % 4] = w + 10**3
            heapq.heappush(pq, (w + 10**3, (ci, cj, (d + 1) % 4)))
            best_graph[(ci, cj, d)].append(1)

        if best[ci][cj][(d - 1) % 4] >= w + 10**3:
            best[ci][cj][(d - 1) % 4] = w + 10**3
            heapq.heappush(pq, (w + 10**3, (ci, cj, (d - 1) % 4)))
            best_graph[(ci, cj, d)].append(2)

    on_some_best = set()
    vis = set()

    def dfs(i: int, j: int, d: int) -> None:
        vis.add((i, j, d))

        if i == ei and j == ej and best[i][j][d] == min(best[i][j]):
            on_some_best.add((i, j, d))
            return

        for t in best_graph[(i, j, d)]:
            ni, nj, nd = -1, -1, -1
            if t == 0:
                ni, nj, nd = i + DI[d], j + DJ[d], d
            elif t == 1:
                ni, nj, nd = i, j, (d + 1) % 4
            elif t == 2:
                ni, nj, nd = i, j, (d - 1) % 4

            if (ni, nj, nd) not in vis:
                dfs(ni, nj, nd)

            if (ni, nj, nd) in on_some_best:
                on_some_best.add((i, j, d))

    dfs(si, sj, 0)

    return Outp(len(set((i, j) for i, j, _ in on_some_best)))


def show_output(outp: Outp) -> None:
    print(outp.ans)


def main():
    show_output(solve(get_input()))


main()
