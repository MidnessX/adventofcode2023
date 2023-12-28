#!/usr/bin/env python3

from pathlib import Path
import numpy as np


def next_cells(
    cell: tuple[int, int], prev_cell: tuple[int, int] | None, trails_map: np.ndarray
) -> list[tuple[int, int]]:
    if trails_map[cell] == ">":
        candidates = [(cell[0], cell[1] + 1)]
    elif trails_map[cell] == "<":
        candidates = [(cell[0], cell[1] - 1)]
    elif trails_map[cell] == "v":
        candidates = [(cell[0] + 1, cell[1])]
    elif trails_map[cell] == "^":
        candidates = [(cell[0] - 1, cell[1])]
    else:
        candidates = [
            (cell[0] + x, cell[1] + y) for x, y in [(0, -1), (-1, 0), (0, 1), (1, 0)]
        ]

    candidates = filter(
        lambda t: 0 <= t[0] < trails_map.shape[0]
        and 0 <= t[1] < trails_map.shape[1]
        and trails_map[t] != "#"
        and t != prev_cell,
        candidates,
    )

    return list(candidates)


def find_max_path(
    start: tuple[int, int],
    end: tuple[int, int],
    trails_map: np.ndarray,
    visited: set[tuple[int, int]],
) -> int:
    cells = [(0, start, None)]
    max_length = 0

    while len(cells) > 0:
        length, cell, prev_cell = cells.pop(0)

        if cell == end:
            max_length = max(max_length, length)

        cells.extend(
            [
                (length + 1, next_cell, cell)
                for next_cell in next_cells(cell, prev_cell, trails_map)
            ]
        )

    return max_length


with open(Path(__file__).parent / "input.txt") as map_f:
    trails_map: list[list[str]] = list()

    for line in map_f:
        line = line.rstrip()
        trails_map.append([cell for cell in line])

trails_map = np.asarray(trails_map)

max_path = find_max_path(
    (0, 1), (trails_map.shape[0] - 1, trails_map.shape[1] - 2), trails_map, set()
)

print(f"Longest path: {max_path}.")
