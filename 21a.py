from dataclasses import dataclass


@dataclass
class Inp:
    codes: list[str]


@dataclass
class Outp:
    ans: int


type Pad = list[list[str]]

NUM: Pad = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], ["?", "0", "A"]]
DIR: Pad = [["?", "^", "A"], ["<", "v", ">"]]


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
    if depth == 3:
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


def shortest_path(code: str, depth: int = 3) -> str:
    if depth == 0:
        return code
    else:
        code = "A" + code
        all_poss = [""]
        for cc, nc in zip(code, code[1:]):
            all_poss = [
                cur + poss
                for cur in all_poss
                for poss in poss_walks(cc, nc, choose_pad(depth))
            ]
        min_len = min(map(len, all_poss))
        best = ""
        for poss in all_poss:
            if len(poss) == min_len:
                res = shortest_path(poss, depth - 1)
                if best == "" or len(res) < len(best):
                    best = res
        return best


def solve(inp: Inp) -> Outp:
    ans = 0
    for code in inp.codes:
        ans += int(code[:-1]) * len(shortest_path(code))
    return Outp(ans)


def show_output(outp: Outp) -> None:
    print(outp.ans)


def main():
    show_output(solve(get_input()))


main()
