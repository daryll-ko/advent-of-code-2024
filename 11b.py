from dataclasses import dataclass
from functools import cache


@dataclass
class Inp:
    start: list[int]


@dataclass
class Outp:
    num: int


def get_input() -> Inp:
    with open("in.txt", "r") as f:
        start = [*map(int, f.readline().strip().split())]
        return Inp(start)


def solve(inp: Inp) -> Outp:
    @cache
    def num_after(n: int, t: int) -> int:
        if t == 0:
            return 1
        else:
            if n == 0:
                return num_after(1, t - 1)
            elif (m := len(s := str(n))) % 2 == 0:
                n1 = int(s[: m // 2])
                n2 = int(s[m // 2 :])

                return num_after(n1, t - 1) + num_after(n2, t - 1)
            else:
                return num_after(2024 * n, t - 1)

    num = sum(map(lambda x: num_after(x, 75), inp.start))

    return Outp(num)


def show_output(outp: Outp) -> None:
    print(outp.num)


def main():
    show_output(solve(get_input()))


main()
