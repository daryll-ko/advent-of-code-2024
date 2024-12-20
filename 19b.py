from dataclasses import dataclass


@dataclass
class Inp:
    patterns: list[str]
    designs: list[str]


@dataclass
class Outp:
    ans: int


def get_input() -> Inp:
    with open("in.txt", "r") as f:
        patterns = f.readline().strip().split(", ")
        f.readline()
        designs = [*map(lambda line: line.strip(), f.readlines())]

        return Inp(patterns, designs)


def num_possible(design: str, patterns: list[str]) -> int:
    n = len(design)

    # dp[i] = num of ways for design[1..i]
    dp = [0 for _ in range(n + 1)]
    dp[0] = 1

    for i in range(1, n + 1):
        for pattern in patterns:
            if len(pattern) <= i and design[i - len(pattern) : i] == pattern:
                dp[i] += dp[i - len(pattern)]

    return dp[-1]


def solve(inp: Inp) -> Outp:
    ans = 0

    for design in inp.designs:
        ans += num_possible(design, inp.patterns)

    return Outp(ans)


def show_output(outp: Outp) -> None:
    print(outp.ans)


def main():
    show_output(solve(get_input()))


main()
