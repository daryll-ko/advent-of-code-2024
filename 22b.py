from collections import defaultdict
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


def all_diffs_and_nums(n: int, steps: int) -> tuple[list[int], list[int]]:
    cur = n

    diffs = []
    nums = []

    for _ in range(steps):
        next = (cur ^ (cur << 6)) % MOD
        next = (next ^ (next >> 5)) % MOD
        next = (next ^ (next << 11)) % MOD

        diffs.append((next % 10) - (cur % 10))
        nums.append(next % 10)

        cur = next

    return diffs, nums


def solve(inp: Inp) -> Outp:
    n = len(inp.secrets)
    l = map(lambda init: all_diffs_and_nums(init, 2000), inp.secrets)

    seq_to_total = defaultdict(int)
    done_seq = [set() for _ in range(n)]

    for i, (diffs, nums) in enumerate(l):
        m = len(diffs)
        for j in range(m - 3):
            seq = tuple(diffs[j : j + 4])
            if seq not in done_seq[i]:
                seq_to_total[seq] += nums[j + 3]
                done_seq[i].add(seq)

    return Outp(max(seq_to_total.values()))


def show_output(outp: Outp) -> None:
    print(outp.ans)


def main():
    show_output(solve(get_input()))


main()
