#!/usr/bin/env python3

from pathlib import Path
from dataclasses import dataclass
import bisect
from typing import Any
from functools import total_ordering
from itertools import cycle
from math import lcm


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

    # List of nodes in the file.
    # Will be kept ordered by node name to speed up the search for a node.
    nodes = list()

    for line in map_f.readlines():
        name, links = line.split("=")

        name = name.rstrip()
        links = links.lstrip().rstrip("\n").lstrip("(").rstrip(")")

        l_link, r_link = links.split(", ")

        bisect.insort_right(nodes, (Node(name, l_link, r_link)))

# Part 1

next_node = "AAA"
steps = 0

for direction in cycle(instr):
    if next_node == "ZZZ":
        break

    node_pos = bisect.bisect_left(nodes, next_node, key=lambda n: n.name)
    node = nodes[node_pos]

    next_node = node.l if direction == "L" else node.r

    steps += 1

print(f"Number of steps required to reach node ZZZ: {steps}")

# Part 2
# Iterating simultaneously through the graph for all the starting nodes would
# require too many iterations.
# Instead, we can find the minimum number of steps to reach a node ending with
# Z for for each of the starting nodes, and then calculate the least common
# multiple of these values to find the number of simultaneous steps we should
# have done.

next_nodes = list(map(lambda n: n.name, filter(lambda n: n.name.endswith("A"), nodes)))
cycle_lengths = list()

for i in range(len(next_nodes)):
    next_node = next_nodes[i]

    for step, direction in enumerate(cycle(instr)):
        node_pos = bisect.bisect_left(nodes, next_node, key=lambda n: n.name)
        node = nodes[node_pos]

        if node.name.endswith("Z"):
            cycle_lengths.append(step)
            break

        next_node = node.l if direction == "L" else node.r

steps = lcm(*cycle_lengths)

print(f"Number of steps required to reach nodes ending with Z: {steps}")
