#!/usr/bin/env python3

from pathlib import Path
import numpy as np

DIRECTIONS = {
    "<": [(0, -1)],
    ">": [(0, 1)],
    "^": [(-1, 0)],
    "v": [(1, 0)],
    ".": [(0, -1), (0, 1), (-1, 0), (1, 0)],
}


def next_cells(
    cell: tuple[int, int],
    trails_map: np.ndarray,
    slopes: bool,
) -> list[tuple[int, tuple[int, int]]]:
    cell_value = trails_map[cell]

    dirs = DIRECTIONS[cell_value if slopes else "."]
    candidates = [(1, (cell[0] + d[0], cell[1] + d[1])) for d in dirs]

    candidates = filter(
        lambda t: 0 <= t[1][0] < trails_map.shape[0]
        and 0 <= t[1][1] < trails_map.shape[1]
        and trails_map[t[1]] != "#",
        candidates,
    )

    candidates = list(candidates)

    return candidates


def contract_graph(
    graph: dict[tuple[int, int], list[tuple[int, tuple[int, int]]]]
) -> None:
    # We want to remove all those nodes which only have two neighbours, as they
    # form a path with no alternatives between them.
    # Recursively doing so leads to a simplified version of the initial graph,
    # only containing the starting node, slopes, intersections and the
    # destinantion node. This, in turn, leads to a faster DFS.

    while True:
        for node, neighs in graph.items():
            if len(neighs) != 2:
                continue

            (dist_prev, prev), (dist_next, next) = neighs

            # Node may not be in neighbours of previous or next when they are
            # a slope tile.
            if (dist_prev, node) in graph[prev]:
                graph[prev].remove((dist_prev, node))
                graph[prev].append((dist_prev + dist_next, next))
            if (dist_next, node) in graph[next]:
                graph[next].remove((dist_next, node))
                graph[next].append((dist_prev + dist_next, prev))

            graph.pop(node)

            break
        else:
            break


def build_graph(
    trails_map: np.ndarray, slopes: bool
) -> dict[tuple[int, int], list[tuple[int, tuple[int, int]]]]:
    # Graph is a mapping from a cell to the list of its neighbouring cells and
    # their respective distances.
    graph: dict[tuple[int, int], list[tuple[int, tuple[int, int]]]] = dict()

    for x in range(trails_map.shape[0]):
        for y in range(trails_map.shape[1]):
            if trails_map[x, y] == "#":
                continue

            graph[(x, y)] = next_cells((x, y), trails_map, slopes=slopes)

    contract_graph(graph)

    return graph


def find_max_path(
    start: tuple[int, int],
    end: tuple[int, int],
    graph: dict[tuple[int, int], tuple[int, tuple[int, int]]],
) -> int:
    cells = [(0, start, set())]
    max_length = 0

    while len(cells) > 0:
        # By popping the last item this sort of works like a stack, hence giving
        # us DFS, which is much faster for this problem than what is achievable
        # by using a queue (BFS).
        length, cell, visited = cells.pop()

        if cell in visited:
            continue

        visited.add(cell)

        if cell == end:
            max_length = max(max_length, length)

        neighbours = [
            (length + distance, next_cell, visited.copy())
            for distance, next_cell in graph[cell]
        ]
        cells.extend(neighbours)

    return max_length


with open(Path(__file__).parent / "input.txt") as map_f:
    trails_map: list[list[str]] = list()

    for line in map_f:
        line = line.rstrip()
        trails_map.append([cell for cell in line])

trails_map = np.asarray(trails_map)

graph = build_graph(trails_map, slopes=True)
longest_path = find_max_path(
    (0, 1), (trails_map.shape[0] - 1, trails_map.shape[1] - 2), graph
)
print(f"Longest path (with slopes): {longest_path}")

graph = build_graph(trails_map, slopes=False)
longest_path = find_max_path(
    (0, 1), (trails_map.shape[0] - 1, trails_map.shape[1] - 2), graph
)
print(f"Longest path (without slopes): {longest_path}")
