from dataclasses import dataclass


@dataclass
class Inp:
    edges: list[tuple[str, str]]


@dataclass
class Outp:
    ans: int


def get_input() -> Inp:
    with open("in.txt", "r") as f:
        edges = []
        for line in f.readlines():
            line = line.strip()
            u, v = line.split("-")
            edges.append((u, v))
        return Inp(edges)


def solve(inp: Inp) -> Outp:
    n = 0
    name_to_index, index_to_name = {}, {}

    for u, v in inp.edges:
        for x in (u, v):
            if x not in name_to_index:
                name_to_index[x] = n
                index_to_name[n] = x
                n += 1

    adj_mat = [[False for _ in range(n)] for _ in range(n)]

    for u, v in inp.edges:
        u, v = name_to_index[u], name_to_index[v]
        adj_mat[u][v] = adj_mat[v][u] = True

    ans = 0
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if (
                    adj_mat[i][j]
                    and adj_mat[j][k]
                    and adj_mat[k][i]
                    and "t"
                    in index_to_name[i][0] + index_to_name[j][0] + index_to_name[k][0]
                ):
                    ans += 1

    return Outp(ans)


def show_output(outp: Outp) -> None:
    print(outp.ans)


def main():
    show_output(solve(get_input()))


main()
