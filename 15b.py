from dataclasses import dataclass


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

            fatten = {"#": "##", "O": "[]", ".": "..", "@": "@."}

            if grid_done:
                moves += list(line)
            else:
                grid.append(list("".join(map(lambda cell: fatten[cell], line))))

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
        else:  # '[]'
            to_push = set()
            push = True

            def dfs(i: int, j: int) -> None:
                to_push.add((i, j))

                nni, nnj = i + DI[move], j + DJ[move]

                if inp.grid[nni][nnj] in "[]" and (nni, nnj) not in to_push:
                    dfs(nni, nnj)

                if inp.grid[i][j] == "[" and (i, j + 1) not in to_push:
                    dfs(i, j + 1)
                elif inp.grid[i][j] == "]" and (i, j - 1) not in to_push:
                    dfs(i, j - 1)

            dfs(ni, nj)

            for i, j in to_push:
                nni, nnj = i + DI[move], j + DJ[move]
                push = push and inp.grid[nni][nnj] != "#"

            if push:
                char_at = {(i, j): inp.grid[i][j] for i, j in to_push}

                for i, j in to_push:
                    inp.grid[i][j] = "."

                for i, j in to_push:
                    nni, nnj = i + DI[move], j + DJ[move]
                    inp.grid[nni][nnj] = char_at[(i, j)]

                inp.grid[ni][nj] = "@"
                inp.grid[ci][cj] = "."
            else:
                continue

        ci, cj = ni, nj

    ans = 0
    for i in range(r):
        for j in range(c):
            if inp.grid[i][j] == "[":
                ans += 100 * i + j

    return Outp(ans)


def show_output(outp: Outp) -> None:
    print(outp.ans)


def main():
    show_output(solve(get_input()))


main()
