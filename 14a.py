from dataclasses import dataclass

import re


@dataclass
class Robot:
    px: int
    py: int
    vx: int
    vy: int

    def step(self, t: int, r: int, c: int) -> None:
        self.px = (self.px + self.vx * t) % c
        self.py = (self.py + self.vy * t) % r


@dataclass
class Inp:
    robots: list[Robot]
    r: int = 103
    c: int = 101
    t: int = 100


@dataclass
class Outp:
    ans: int


def get_input() -> Inp:
    with open("in.txt", "r") as f:
        exp = re.compile(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)")
        robots = []

        for line in f.readlines():
            if (m := exp.match(line.strip())) is not None:
                px, py, vx, vy = map(int, m.groups())
                robots.append(Robot(px, py, vx, vy))

        return Inp(robots)


def solve(inp: Inp) -> Outp:
    tl, tr, bl, br = 0, 0, 0, 0

    for robot in inp.robots:
        robot.step(inp.t, inp.r, inp.c)

        if robot.px < inp.c // 2 and robot.py < inp.r // 2:
            tl += 1
        elif robot.px < inp.c // 2 and robot.py > inp.r // 2:
            bl += 1
        elif robot.px > inp.c // 2 and robot.py < inp.r // 2:
            tr += 1
        elif robot.px > inp.c // 2 and robot.py > inp.r // 2:
            br += 1

    return Outp(tl * tr * bl * br)


def show_output(outp: Outp) -> None:
    print(outp.ans)


def main():
    show_output(solve(get_input()))


main()
