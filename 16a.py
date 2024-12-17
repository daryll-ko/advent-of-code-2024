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

    while len(pq) > 0:
        w, (ci, cj, d) = heapq.heappop(pq)

        if ci == ei and cj == ej:
            continue

        ni, nj = ci + DI[d], cj + DJ[d]

        if inp.grid[ni][nj] != "#" and best[ni][nj][d] > w + 1:
            best[ni][nj][d] = w + 1
            heapq.heappush(pq, (w + 1, (ni, nj, d)))

        if best[ci][cj][(d + 1) % 4] > w + 10**3:
            best[ci][cj][(d + 1) % 4] = w + 10**3
            heapq.heappush(pq, (w + 10**3, (ci, cj, (d + 1) % 4)))

        if best[ci][cj][(d - 1) % 4] > w + 10**3:
            best[ci][cj][(d - 1) % 4] = w + 10**3
            heapq.heappush(pq, (w + 10**3, (ci, cj, (d - 1) % 4)))

    ans = INF
    for d in range(4):
        ans = min(ans, best[ei][ej][d])

    return Outp(ans)


def show_output(outp: Outp) -> None:
    print(outp.ans)


def main():
    show_output(solve(get_input()))


main()
