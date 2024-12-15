from dataclasses import dataclass

import re
import time
import sys


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


@dataclass
class Outp: ...


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
    for t in range(1, 10**4 + 1):
        grid = [[0 for _ in range(inp.c)] for _ in range(inp.r)]

        for robot in inp.robots:
            robot.step(1, inp.r, inp.c)
            grid[robot.py][robot.px] += 1

        print(f"t = {t}")
        print()
        for row in grid:
            print("".join(map(lambda x: "." if x == 0 else str(x), row)))
        print()

    return Outp()


def show_output(outp: Outp) -> None:
    return


def main():
    show_output(solve(get_input()))


main()
