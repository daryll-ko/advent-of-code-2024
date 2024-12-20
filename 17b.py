from dataclasses import dataclass
from typing import Optional


@dataclass
class Inp: ...


@dataclass
class Outp:
    ans: int


BITS = 3 * 16
GOAL = [2, 4, 1, 6, 7, 5, 4, 4, 1, 7, 0, 3, 5, 5, 3, 0]


def get_input() -> Inp:
    return Inp()


def xor(a: list[int], b: list[int]) -> list[int]:
    assert len(a) == len(b)

    return [x ^ y for x, y in zip(a, b)]


def bits_to_val(bits: list[int]) -> int:
    ans = 0
    for i, bit in enumerate(bits):
        if bit == -1:
            break
        ans += bit * (1 << i)
    return ans


def val_to_bits(val: int, size: int = 3) -> list[int]:
    b = []

    while val > 0:
        b.append(val % 2)
        val //= 2

    while len(b) < size:
        b.append(0)

    return b


def solve(inp: Inp) -> Outp:
    def backtrack(i: int, bits: list[int]) -> Optional[list[int]]:
        if i >= BITS:
            if all(b != -1 for b in bits[:BITS]):
                return bits

        for poss in range(8):
            l = val_to_bits(poss)

            l = xor(l, val_to_bits(6))
            offset = bits_to_val(l)

            l = xor(l, val_to_bits(7))
            l = xor(l, val_to_bits(GOAL[i // 3]))

            updates = []

            ok = True

            # inconsistency bet existing & planned
            for base, what_to_set in zip((i, i + offset), (val_to_bits(poss), l)):
                for j in range(3):
                    updates.append((base + j, what_to_set[j]))
                    if bits[base + j] != -1 and bits[base + j] != what_to_set[j]:
                        ok = False

            # inconsistency within planned
            for b1, s1 in updates:
                for b2, s2 in updates:
                    if b1 == b2 and s1 != s2:
                        ok = False

            if not ok:
                continue

            to_revert = []

            for base, what_to_set in zip((i, i + offset), (val_to_bits(poss), l)):
                for j in range(3):
                    if bits[base + j] == -1:
                        to_revert.append(base + j)
                    bits[base + j] = what_to_set[j]

            if (res := backtrack(i + 3, bits)) is not None:
                return res

            for pos in to_revert:
                bits[pos] = -1

    ans_bits = backtrack(0, [-1 for _ in range(64)])

    assert ans_bits is not None

    return Outp(bits_to_val(ans_bits))


def show_output(outp: Outp) -> None:
    print(outp.ans)


def main():
    show_output(solve(get_input()))


main()
