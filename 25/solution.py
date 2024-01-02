#!/usr/bin/env python3

from pathlib import Path
from collections import defaultdict

conns = defaultdict(set)
with open(Path(__file__).parent / "input.txt") as comp_f:
    for line in comp_f.readlines():
        item, others = line.rstrip().split(":")
        others = others.lstrip(" ").split()

        for other in others:
            conns[item].add(other)
            conns[other].add(item)

# We want two components (A and B) of the original graph which only have three
# connections between each other.
# We start with component A containing all the items.
comp_a = set(conns.keys())

while True:
    # For each item, we calculate the number of connections to items outside
    # component A (i.e. in component B).
    ext_conns = {x: len(conns[x] - comp_a) for x in comp_a}

    # If the total number of these connections is exactly 3, we can have found
    # our solution.
    if sum(ext_conns.values()) == 3:
        break

    # We find the item having the most outside connections and remove it as it
    # most certainly belongs to the other component.
    # N.B. during the first iteration, the item to remove is chosen
    # pseudo-randomly as all the external connections are 0.
    # Sometimes, a node actually belonging to component A is chosen, leading to
    # an exception. If this happens, simply run the script again.
    item = max(ext_conns.keys(), key=lambda x: ext_conns[x])
    comp_a.remove(item)


c_a_size = len(comp_a)
c_b_size = len(set(conns.keys()) - comp_a)

print(f"Multiplication of component A and component B sizes: {c_a_size * c_b_size}.")
