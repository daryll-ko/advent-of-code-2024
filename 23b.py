from dataclasses import dataclass

import networkx as nx


@dataclass
class Inp:
    edges: list[tuple[str, str]]


@dataclass
class Outp:
    ans: str


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

    edges = []

    for u, v in inp.edges:
        u, v = name_to_index[u], name_to_index[v]
        edges.append((u, v))

    G = nx.Graph()
    G.add_edges_from(edges)

    cliques = [*nx.find_cliques(G)]
    sizes = map(len, cliques)
    longest = max(sizes)

    ans = ""

    for clique in cliques:
        if len(clique) == longest:
            ans = ",".join(sorted(map(lambda i: index_to_name[i], clique)))

    return Outp(ans)


def show_output(outp: Outp) -> None:
    print(outp.ans)


def main():
    show_output(solve(get_input()))


main()
