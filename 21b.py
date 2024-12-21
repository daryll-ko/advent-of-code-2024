from dataclasses import dataclass
from functools import cache


@dataclass
class Inp:
    codes: list[str]


@dataclass
class Outp:
    ans: int


type Pad = list[list[str]]

NUM: Pad = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], ["?", "0", "A"]]
DIR: Pad = [["?", "^", "A"], ["<", "v", ">"]]

INF = 10**20


def get_pos(char: str, pad: Pad) -> tuple[int, int]:
    r, c = len(pad), len(pad[0])
    for i in range(r):
        for j in range(c):
            if pad[i][j] == char:
                return (i, j)
    assert False


def get_input() -> Inp:
    with open("in.txt", "r") as f:
        codes = [*map(lambda line: line.strip(), f.readlines())]
    return Inp(codes)


def choose_pad(depth: int) -> Pad:
    if depth == 26:
        return NUM
    else:
        return DIR


def walkable(i: int, j: int, path: str, pad: Pad) -> bool:
    DIJ = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}

    ci, cj = i, j

    for c in path:
        di, dj = DIJ[c]
        ni, nj = ci + di, cj + dj
        if pad[ni][nj] == "?":
            return False
        ci, cj = ni, nj

    return True


def poss_walks(cc: str, nc: str, pad: Pad) -> list[str]:
    (i1, j1), (i2, j2) = get_pos(cc, pad), get_pos(nc, pad)
    s = abs(i1 - i2) * ("^" if i1 > i2 else "v") + abs(j1 - j2) * (
        "<" if j1 > j2 else ">"
    )
    choices = sorted(list({"".join(sorted(s)), "".join(reversed(sorted(s)))}))
    ans = []
    for poss in choices:
        if walkable(i1, j1, poss, pad):
            ans.append(poss + "A")
    return ans


@cache
def _len_shortest_path(cc: str, nc: str, depth: int) -> int:
    if depth == 0:
        return 1
    else:
        all_poss = poss_walks(cc, nc, choose_pad(depth))
        ans = INF

        for poss in all_poss:
            poss = "A" + poss
            cur = 0
            for _cc, _nc in zip(poss, poss[1:]):
                cur += _len_shortest_path(_cc, _nc, depth - 1)
            ans = min(ans, cur)

        return ans


def len_shortest_path(code: str, depth: int = 26) -> int:
    if depth == 0:
        return len(code)
    else:
        code = "A" + code
        ans = 0
        for cc, nc in zip(code, code[1:]):
            ans += _len_shortest_path(cc, nc, depth)
        return ans


def solve(inp: Inp) -> Outp:
    ans = 0
    for code in inp.codes:
        ans += int(code[:-1]) * len_shortest_path(code)
    return Outp(ans)


def show_output(outp: Outp) -> None:
    print(outp.ans)


def main():
    show_output(solve(get_input()))


main()
