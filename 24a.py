from collections import defaultdict
from dataclasses import dataclass
from enum import Enum, auto
from typing import Protocol


class Node(Protocol):
    name: str

    def get_value(self) -> int: ...


class NodeType(Enum):
    AND = auto()
    OR = auto()
    XOR = auto()


@dataclass
class InputNode:
    name: str

    val: int

    def get_value(self) -> int:
        return self.val


@dataclass
class InnerNode:
    name: str

    kind: NodeType
    in1: int
    in2: int

    def get_value(self) -> int:
        match self.kind:
            case NodeType.AND:
                return self.in1 & self.in2
            case NodeType.OR:
                return self.in1 | self.in2
            case NodeType.XOR:
                return self.in1 ^ self.in2


@dataclass
class Edge:
    u: str
    v: str


@dataclass
class Inp:
    input_nodes: list[InputNode]
    inner_nodes: list[InnerNode]
    edges: list[Edge]


@dataclass
class Outp:
    ans: int


def get_input() -> Inp:
    with open("in.txt", "r") as f:
        lines = f.readlines()
        input_nodes_done = False

        input_nodes = []
        inner_nodes = []
        edges = []

        for line in lines:
            line = line.strip()

            if len(line) == 0:
                input_nodes_done = True
                continue

            if input_nodes_done:  # inner node
                u1, kind, u2, _, v = line.split()

                edges.append(Edge(u1, v))
                edges.append(Edge(u2, v))

                match kind:
                    case "AND":
                        inner_nodes.append(InnerNode(v, NodeType.AND, -1, -1))
                    case "OR":
                        inner_nodes.append(InnerNode(v, NodeType.OR, -1, -1))
                    case "XOR":
                        inner_nodes.append(InnerNode(v, NodeType.XOR, -1, -1))
                    case _:
                        assert False
            else:  # input node
                u, val = line.split()

                u = u[:-1]
                val = int(val)

                input_nodes.append(InputNode(u, val))

        return Inp(input_nodes, inner_nodes, edges)


def solve(inp: Inp) -> Outp:
    adj_list = defaultdict(list)

    for edge in inp.edges:
        for name in (edge.u, edge.v):
            if name not in adj_list:
                adj_list[name] = []

        adj_list[edge.u].append(edge.v)

    name_to_node: dict[str, Node] = {}

    for input_node in inp.input_nodes:
        name_to_node[input_node.name] = input_node

    for inner_node in inp.inner_nodes:
        name_to_node[inner_node.name] = inner_node

    toposort = []
    vis = set()

    def dfs(u: str) -> None:
        vis.add(u)

        for v in adj_list[u]:
            if v not in vis:
                dfs(v)

        toposort.append(u)

    for u in adj_list.keys():
        if u not in vis:
            dfs(u)

    toposort.reverse()

    for u in toposort:
        val = name_to_node[u].get_value()

        for v in adj_list[u]:
            node = name_to_node[v]

            assert isinstance(node, InnerNode)

            if node.in1 == -1:
                node.in1 = val
            elif node.in2 == -1:
                node.in2 = val
            else:
                assert False

    for u in toposort:
        node = name_to_node[u]

    ans = 0

    for i in range(10**2):
        name = f"z{str(i).zfill(2)}"

        if name in name_to_node:
            ans += name_to_node[name].get_value() * (1 << i)

    return Outp(ans)


def show_output(outp: Outp) -> None:
    print(outp.ans)


def main():
    show_output(solve(get_input()))


main()
