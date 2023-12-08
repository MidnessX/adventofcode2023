#!/usr/bin/env python3

from pathlib import Path
from dataclasses import dataclass
import bisect
from typing import Any
from functools import total_ordering


@dataclass
@total_ordering
class Node:
    name: str
    l: str
    r: str

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Node):
            return False

        if self.name == other.name:
            return True

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, Node):
            raise NotImplementedError()

        return self.name > other.name


with open(Path(__file__).parent / "input.txt") as map_f:
    instr = tuple(char for char in map_f.readline().rstrip("\n"))

    map_f.readline()  # Consume an empty line

    nodes = list()

    for line in map_f.readlines():
        name, links = line.split("=")

        name = name.rstrip()
        links = links.lstrip().rstrip("\n").lstrip("(").rstrip(")")

        l_link, r_link = links.split(", ")

        bisect.insort_right(nodes, (Node(name, l_link, r_link)))

# Part 1

next_node = "AAA"
next_i = 0
steps = 0

while next_node != "ZZZ":
    node_pos = bisect.bisect_left(nodes, next_node, key=lambda n: n.name)
    node = nodes[node_pos]

    next_node = node.l if instr[next_i] == "L" else node.r
    next_i = (next_i + 1) % len(instr)

    steps += 1

print(f"Number of steps required to reach node ZZZ: {steps}")
