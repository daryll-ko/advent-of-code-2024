from collections import deque
from dataclasses import dataclass


@dataclass
class Inp:
    incoming: list[tuple[int, int]]
    R: int = 71
    C: int = 71
    first: int = 1 << 10


@dataclass
class Outp:
    ans: int


INF = 10**20
DIJ = [(0, 1), (-1, 0), (0, -1), (1, 0)]


def get_input() -> Inp:
    with open("in.txt", "r") as f:
        incoming = []

        for line in f.readlines():
            line = line.strip()
            j, i = map(int, line.split(","))
            incoming.append((i, j))

        return Inp(incoming)


def solve(inp: Inp) -> Outp:
    grid = [["." for _ in range(inp.C)] for _ in range(inp.R)]

    for i, j in inp.incoming[: inp.first]:
        grid[i][j] = "#"

    dis = [[INF for _ in range(inp.C)] for _ in range(inp.R)]
    q = deque()

    dis[0][0] = 0
    q.append((0, 0))

    def within_bounds(i: int, j: int) -> bool:
        return 0 <= i < inp.R and 0 <= j < inp.C

    while len(q) > 0:
        i, j = q.popleft()

        for di, dj in DIJ:
            ni, nj = i + di, j + dj
            if (
                within_bounds(ni, nj)
                and grid[i][j] != "#"
                and dis[ni][nj] > dis[i][j] + 1
            ):
                dis[ni][nj] = dis[i][j] + 1
                q.append((ni, nj))

    return Outp(dis[-1][-1])


def show_output(outp: Outp) -> None:
    print(outp.ans)


def main():
    show_output(solve(get_input()))


main()
