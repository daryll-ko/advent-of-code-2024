from dataclasses import dataclass


@dataclass
class Inp:
    secrets: list[int]


@dataclass
class Outp:
    ans: int


MOD = 16777216


def get_input() -> Inp:
    with open("in.txt", "r") as f:
        secrets = [*map(lambda line: int(line.strip()), f.readlines())]

        return Inp(secrets)


def next(n: int, steps: int) -> int:
    cur = n
    for _ in range(steps):
        cur = (cur ^ (cur << 6)) % MOD
        cur = (cur ^ (cur >> 5)) % MOD
        cur = (cur ^ (cur << 11)) % MOD
    return cur


def solve(inp: Inp) -> Outp:
    l = map(lambda init: next(init, 2000), inp.secrets)
    return Outp(sum(l))


def show_output(outp: Outp) -> None:
    print(outp.ans)


def main():
    show_output(solve(get_input()))


main()
