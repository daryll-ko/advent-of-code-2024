from dataclasses import dataclass

type Edge = tuple[int, int]


@dataclass
class Inp:
    rules: list[tuple[int, int]]
    updates: list[list[int]]


@dataclass
class Outp:
    ans: int


def get_input() -> Inp:
    rules = []
    updates = []

    rules_done = False

    with open("in.txt", "r") as f:
        for line in f.readlines():
            line = line.strip()

            if len(line) == 0:
                rules_done = True
                continue

            if rules_done:
                updates.append([*map(int, line.split(","))])
            else:
                rules.append(tuple(map(int, line.split("|"))))

    return Inp(rules, updates)


def toposort(es: list[Edge]) -> list[int]:
    vs = set()
    for a, b in es:
        vs.add(a)
        vs.add(b)

    adj = {v: [] for v in vs}
    for a, b in es:
        adj[a].append(b)

    vis = {v: False for v in vs}
    ans = []

    def dfs(u: int) -> None:
        vis[u] = True
        for v in adj[u]:
            if not vis[v]:
                dfs(v)
        ans.append(u)

    for v in vs:
        if not vis[v]:
            dfs(v)

    return [*reversed(ans)]


def solve(inp: Inp) -> Outp:
    ans = 0

    for update in inp.updates:
        topo = toposort([(a, b) for (a, b) in inp.rules if a in update and b in update])
        u_to_index = {u: i for u, i in zip(topo, range(len(topo)))}
        indices = [*map(lambda u: u_to_index[u], update)]

        if sorted(indices) != indices:
            fixed = [topo[index] for index in sorted(indices)]
            ans += fixed[len(fixed) // 2]

    return Outp(ans)


def show_output(outp: Outp) -> None:
    print(outp.ans)


def main():
    show_output(solve(get_input()))


main()
