from dataclasses import dataclass


@dataclass
class Inp:
    queries: list[tuple[int, list[int]]]


@dataclass
class Outp:
    ans: int


def get_input() -> Inp:
    with open("in.txt", "r") as f:
        queries = []

        for line in f.readlines():
            line = line.strip()
            goal, operands = line.split(": ")

            goal = int(goal)
            operands = [*map(int, operands.split())]

            queries.append((goal, operands))

        return Inp(queries)


def doable(goal: int, operands: list[int]) -> bool:
    n = len(operands)

    for i in range(3 ** (n - 1)):
        cur = operands[0]
        for j in range(n - 1):
            digit = (i // (3**j)) % 3
            if digit == 0:
                cur += operands[j + 1]
            elif digit == 1:
                cur *= operands[j + 1]
            else:
                cur = int(str(cur) + str(operands[j + 1]))
        if cur == goal:
            return True

    return False


def solve(inp: Inp) -> Outp:
    ans = 0
    for goal, operands in inp.queries:
        if doable(goal, operands):
            ans += goal
    return Outp(ans)


def show_output(outp: Outp) -> None:
    print(outp.ans)


def main():
    show_output(solve(get_input()))


main()
