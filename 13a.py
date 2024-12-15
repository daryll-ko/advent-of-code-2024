import re

from dataclasses import dataclass


@dataclass
class Machine:
    dx1: int
    dy1: int

    dx2: int
    dy2: int

    tx: int
    ty: int


@dataclass
class Inp:
    machines: list[Machine]


@dataclass
class Outp:
    ans: int


def get_input() -> Inp:
    with open("in.txt", "r") as f:
        lines = f.readlines()
        machines = []

        for i in range(0, len(lines), 4):
            exp = re.compile(r".*X[\+=](\d+), Y[\+=](\d+)")

            dx1, dy1, dx2, dy2, tx, ty = -1, -1, -1, -1, -1, -1

            if (m := exp.match(lines[i])) is not None:
                dx1, dy1 = map(int, m.groups())
            if (m := exp.match(lines[i + 1])) is not None:
                dx2, dy2 = map(int, m.groups())
            if (m := exp.match(lines[i + 2])) is not None:
                tx, ty = map(int, m.groups())

            machines.append(Machine(dx1, dy1, dx2, dy2, tx, ty))

        return Inp(machines)


INF = 10**10


def best(m: Machine) -> int:
    res = INF
    for a in range(100 + 1):
        for b in range(100 + 1):
            if a * m.dx1 + b * m.dx2 == m.tx and a * m.dy1 + b * m.dy2 == m.ty:
                res = min(res, 3 * a + b)
    return res


def solve(inp: Inp) -> Outp:
    ans = sum(
        map(lambda machine: val if (val := best(machine)) != INF else 0, inp.machines)
    )
    return Outp(ans)


def show_output(outp: Outp) -> None:
    print(outp.ans)


def main():
    show_output(solve(get_input()))


main()
