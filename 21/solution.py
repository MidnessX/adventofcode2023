#!/usr/bin/env python3

from pathlib import Path

import numpy as np


def neighbouring_tiles(
    tile: tuple[int, int], garden: np.ndarray
) -> list[tuple[int, int]]:
    candidates = [
        (tile[0] + d[0], tile[1] + d[1]) for d in [(-1, 0), (0, 1), (1, 0), (0, -1)]
    ]

    candidates = list(
        filter(
            lambda t: 0 <= t[0] < garden.shape[0]
            and 0 <= t[1] < garden.shape[1]
            and garden[t] != "#",
            candidates,
        )
    )

    return candidates


def reachable_tiles(
    start: tuple[int, int], steps: int, garden: np.ndarray
) -> set[tuple[int, int]]:
    edge_tiles = set([start])

    for _ in range(steps):
        reached_tiles = set()

        for t in edge_tiles:
            neigh = neighbouring_tiles(t, garden)
            reached_tiles.update(neigh)

        edge_tiles = reached_tiles

    return edge_tiles


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

tiles = reachable_tiles(start, 64, garden)

print(f"Reachable tiles: {len(tiles)}.")
