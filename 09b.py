from dataclasses import dataclass


@dataclass
class Inp:
    rle: list[tuple[int, int]]
    #                ID  len


@dataclass
class Outp:
    checksum: int


def get_input() -> Inp:
    rle = []

    with open("in.txt", "r") as f:
        line = f.readline().strip()
        counts = map(int, list(line))

        for i, count in enumerate(counts):
            if i % 2 == 0:
                rle.append((i // 2, count))
            else:
                rle.append((-1, count))

    rle = [(id, count) for id, count in rle if count > 0]

    return Inp(rle)


def sum_until(n: int) -> int:
    return n * (n + 1) // 2


def solve(inp: Inp) -> Outp:
    i = 0
    new_rle = []

    while i < len(inp.rle):
        if inp.rle[-1][0] == -1:
            inp.rle.pop()
            continue

        id, count = inp.rle[i]
        if id == -1:
            if inp.rle[-1][0] == -1:
                inp.rle.pop()

            searching = True

            while count > 0 and searching:
                j = len(inp.rle) - 1
                found = False
                while j > i:
                    l_id, l_count = inp.rle[j]
                    if l_id != -1 and l_count <= count:
                        new_rle.append((l_id, l_count))
                        inp.rle[j] = (-1, l_count)
                        count -= l_count
                        found = True
                        break
                    j -= 1
                searching = searching and found

            if count > 0:
                new_rle.append((-1, count))
        else:
            new_rle.append((id, count))

        i += 1

    checksum = 0
    done = 0
    for id, count in new_rle:
        # id * [done, done + count)
        if id != -1:
            checksum += id * (sum_until(done + count - 1) - sum_until(done - 1))
        done += count

    return Outp(checksum)


def show_output(outp: Outp) -> None:
    print(outp.checksum)


def main():
    show_output(solve(get_input()))


main()
