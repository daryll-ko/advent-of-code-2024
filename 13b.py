import math
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

                tx += 10**13
                ty += 10**13

            machines.append(Machine(dx1, dy1, dx2, dy2, tx, ty))

        return Inp(machines)


INF = 10**20


def extended_euclid(a: int, b: int) -> tuple[int, int]:
    if b == 0:
        return 1, 0
    else:
        x, y = extended_euclid(b, a % b)
        return y, x - (a // b) * y


def best(m: Machine) -> int:
    det = m.dx1 * m.dy2 - m.dx2 * m.dy1

    if det == 0:
        if m.dy1 * m.tx == m.dx1 * m.ty:  # consistent
            g = math.gcd(m.dx1, m.dx2)

            if m.tx % g != 0:
                return INF

            # to offset this, scale answer by g at the end
            m.dx1 //= g
            m.dx2 //= g
            m.tx //= g

            a, b = extended_euclid(m.dx1, m.dx2)

            k = a // m.dx2

            a -= k * m.dx2
            b += k * m.dx1

            return g * (3 * a + b)
        else:
            return INF
    else:  # unique
        dx_lcm = math.lcm(m.dx1, m.dy1)

        num = (dx_lcm // m.dx1) * m.tx - (dx_lcm // m.dy1) * m.ty
        den = (dx_lcm // m.dx1) * m.dx2 - (dx_lcm // m.dy1) * m.dy2

        if den == 0 or num % den != 0 or (b := num // den) < 0:
            return INF
        else:
            num = m.tx - m.dx2 * b
            den = m.dx1

            if den == 0 or num % den != 0 or (a := num // den) < 0:
                return INF
            else:
                return 3 * a + b


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
