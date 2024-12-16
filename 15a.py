from dataclasses import dataclass
from enum import Enum, auto


class Dir(Enum):
    EAST = auto()
    SOUTH = auto()
    WEST = auto()
    NORTH = auto()


@dataclass
class Inp:
    grid: list[list[str]]
    moves: list[str]


@dataclass
class Outp:
    ans: int


DI = [0, 1, 0, -1]
DJ = [1, 0, -1, 0]


def get_input() -> Inp:
    with open("in.txt", "r") as f:
        grid = []
        moves = []
        grid_done = False

        for line in f.readlines():
            line = line.strip()

            if len(line) == 0:
                grid_done = True
                continue

            if grid_done:
                moves += list(line)
            else:
                grid.append(list(line))

        return Inp(grid, moves)


def solve(inp: Inp) -> Outp:
    r, c = len(inp.grid), len(inp.grid[0])

    si, sj = -1, -1
    for i in range(r):
        if si != -1:
            break
        for j in range(c):
            if inp.grid[i][j] == "@":
                si, sj = i, j
                break

    char_to_index = {c: i for i, c in enumerate([">", "v", "<", "^"])}
    moves = [char_to_index[move] for move in inp.moves]

    ci, cj = si, sj
    for move in moves:
        ni, nj = ci + DI[move], cj + DJ[move]

        if inp.grid[ni][nj] == ".":
            inp.grid[ni][nj] = "@"
            inp.grid[ci][cj] = "."
        elif inp.grid[ni][nj] == "#":
            continue
        else:  # 'O'
            s = 2
            push = True

            while True:
                nni, nnj = ci + s * DI[move], cj + s * DJ[move]
                if inp.grid[nni][nnj] == ".":
                    break
                elif inp.grid[nni][nnj] == "#":
                    push = False
                    break

                s += 1

            if push:
                for rep in range(s, 0, -1):
                    nni, nnj = ci + rep * DI[move], cj + rep * DJ[move]
                    if rep == 1:
                        inp.grid[nni][nnj] = "@"
                    else:
                        inp.grid[nni][nnj] = "O"
                inp.grid[ci][cj] = "."
            else:
                continue

        ci, cj = ni, nj

    ans = 0
    for i in range(r):
        for j in range(c):
            if inp.grid[i][j] == "O":
                ans += 100 * i + j

    return Outp(ans)


def show_output(outp: Outp) -> None:
    print(outp.ans)


def main():
    show_output(solve(get_input()))


main()
