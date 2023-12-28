#!/usr/bin/env python3

from pathlib import Path
import numpy as np

SLOPES = {"<": (0, -1), ">": (0, 1), "^": (-1, 0), "v": (1, 0)}


def next_cells(
    cell: tuple[int, int],
    visited: set[tuple[int, int]],
    trails_map: np.ndarray,
    no_slopes: bool,
) -> list[tuple[int, int]]:
    cell_value = trails_map[cell]

    if no_slopes or cell_value not in SLOPES:
        candidates = [
            (cell[0] + x, cell[1] + y) for x, y in [(0, -1), (-1, 0), (0, 1), (1, 0)]
        ]
    else:
        direction = SLOPES[cell_value]
        candidates = [(cell[0] + direction[0], cell[1] + direction[1])]

    candidates = filter(
        lambda t: 0 <= t[0] < trails_map.shape[0]
        and 0 <= t[1] < trails_map.shape[1]
        and trails_map[t] != "#"
        and t not in visited,
        candidates,
    )

    return list(candidates)


def find_max_path(
    start: tuple[int, int],
    end: tuple[int, int],
    trails_map: np.ndarray,
    no_slopes: bool,
) -> int:
    cells = [(0, start, set())]
    max_length = 0

    while len(cells) > 0:
        length, cell, visited = cells.pop(0)

        visited.add(cell)

        if cell == end:
            max_length = max(max_length, length)

        cells.extend(
            [
                (length + 1, next_cell, visited.copy())
                for next_cell in next_cells(
                    cell, visited, trails_map, no_slopes=no_slopes
                )
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
    (0, 1),
    (trails_map.shape[0] - 1, trails_map.shape[1] - 2),
    trails_map,
    no_slopes=False,
)

print(f"Longest path: {max_path}.")

max_path = find_max_path(
    (0, 1),
    (trails_map.shape[0] - 1, trails_map.shape[1] - 2),
    trails_map,
    no_slopes=True,
)

print(f"Longest path (no slopes): {max_path}.")
