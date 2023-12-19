#!/usr/bin/env python3

from pathlib import Path

import numpy as np

directions: dict[str, tuple[int, int]] = {
    "U": (-1, 0),
    "R": (0, 1),
    "D": (1, 0),
    "L": (0, -1),
}

with open(Path(__file__).parent / "input.txt") as instr_f:
    x = 0
    y = 0
    trench = [(x, y)]

    for inst in instr_f.readlines():
        d, count, color = inst.rstrip().split(" ")
        dx, dy = directions.get(d)

        for i in range(int(count)):
            x += dx
            y += dy

            trench.append((x, y))

# The starting point has been added twice, so we remove its last occurrence.
trench.pop()

x = np.asarray(list(map(lambda t: t[0], trench)))
y = np.asarray(list(map(lambda t: t[1], trench)))

# Shoelace formula to find the area of the pool.
area = 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

# From Pick's theorem we can derive the number of internal points.
in_pts = area - (len(trench) / 2) + 1

print(f"Pool squares: {in_pts + len(trench)}.")
