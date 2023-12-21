#!/usr/bin/env python3

from pathlib import Path

import numpy as np


def neighbouring_plots(
    tile: tuple[int, int], garden: np.ndarray, cycle: bool = False
) -> list[tuple[int, int]]:
    candidates = list()

    for d in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        c = (tile[0] + d[0], tile[1] + d[1])

        if not cycle and not (
            0 <= c[0] < garden.shape[0] and 0 <= c[1] < garden.shape[1]
        ):
            continue

        # We use the modulo value to look up the equivalent plot in an adjacent
        # garden tile.
        if garden[(c[0] % garden.shape[0], c[1] % garden.shape[1])] == "#":
            continue

        candidates.append(c)

    return candidates


def reachable_plots(
    start: list[tuple[int, int]], garden: np.ndarray, infinite_garden: bool = False
) -> set[tuple[int, int]]:
    reached_plots = set()

    for t in start:
        neigh = neighbouring_plots(t, garden, cycle=infinite_garden)
        reached_plots.update(neigh)

    return reached_plots


def interpolate(y: list[tuple[int, int]], x: int) -> float:
    a = (y[2] + y[0] - 2 * y[1]) / 2
    b = y[1] - y[0] - a
    c = y[0]

    return a * x**2 + b * x + c


with open(Path(__file__).parent / "input.txt") as map_f:
    garden = list()
    start = (None, None)

    for x, line in enumerate(map_f.readlines()):
        row = list()

        line = line.rstrip()

        for y, c in enumerate(line):
            if c == "S":
                start = (x, y)

            row.append(c)

        garden.append(row)

garden = np.asarray(garden)

# Part 1
goal = 64
starting_plots = set([start])
for _ in range(goal):
    plots = reachable_plots(starting_plots, garden, infinite_garden=False)
    starting_plots = plots

print(f"Reachable plots after {goal} steps: {len(starting_plots)}.")

# Part 2
# The trick here is realizing that the number of reachable plots increases
# quadratically with the number of garden widths walked.
# This is due to how the garden is laid out: edges don't contain rocks, the
# starting point is in the middle and there are no rocks in the row and column
# where the starting point is located. Moreover, diagonal lines connecting
# the middle points of the edges of the garden are also free of rocks.
# This translates to reachable plots expanding in a diamond pattern from the
# center.
# So what we can do is find the first three values of reachable plots and
# use them to fit a quadratic polynomial. Then, we can simply use this
# polynomial to interpolate the number of reachable plots after the desired
# number of steps.

goal = 26501365
starting_plots = set([start])
y = list()
for i in range(1, garden.shape[0] * 3):
    plots = reachable_plots(starting_plots, garden, infinite_garden=True)
    starting_plots = plots

    if i % garden.shape[0] == goal % garden.shape[0]:
        y.append(len(plots))

print(f"Reachable tiles after {goal} steps: {interpolate(y, goal // garden.shape[0])}.")
