#!/usr/bin/env python3

import heapq
from pathlib import Path


def get_neighbours(
    x: int,
    y: int,
    dx: int,
    dy: int,
    s: int,
    min_s: int,
    max_s: int,
    max_x: int,
    max_y: int,
) -> list[tuple[int, int]]:
    n = list()

    if dx == 0 and dy == 0:
        # We are at the start. We can move in any direction.
        n.append((x, y + 1))
        n.append((x, y - 1))
        n.append((x + 1, y))
        n.append((x - 1, y))
    else:
        if s >= min_s:
            n.append((x - dy, y + dx))
            n.append((x + dy, y - dx))
        if s < max_s:
            n.append((x + dx, y + dy))

    n = filter(lambda t: t[0] >= 0 and t[0] < max_x and t[1] >= 0 and t[1] < max_y, n)

    return n


def find_path(
    start: tuple[int, int],
    end: tuple[int, int],
    grid: list[list[int]],
    max_s: int,
    min_s: int = 0,
) -> int:
    # This is a weird Djikstra since we have constraints on the neighbours we
    # can consider depending on previous moves.
    # This means a node can be considered multiple times as long as the
    # direction we came from and the number of steps in that direction differ
    # from those seen previously.

    # In nodes, our priority queue, we keep the cost, the coordinates, the
    # direction we came from and the number of steps we already took in that
    # direction.
    nodes = [(0, *start, 0, 0, 0)]
    # Visited holds the nodes we already explored and the configuration by
    # which they got explored (i.e. the direction and the number of steps in
    # that direction already taken).
    visited = set()

    while nodes:
        c, x, y, dx, dy, s = heapq.heappop(nodes)

        if (x, y, dx, dy, s) in visited:
            continue

        visited.add((x, y, dx, dy, s))

        if (x, y) == end and s >= min_s:
            return c

        for nx, ny in get_neighbours(
            x, y, dx, dy, s, min_s, max_s, len(grid), len(grid[0])
        ):
            nc = c + grid[nx][ny]
            ndx = nx - x
            ndy = ny - y
            ns = s + 1 if dx == ndx and dy == ndy else 1

            heapq.heappush(nodes, (nc, nx, ny, ndx, ndy, ns))


city = list()
with open(Path(__file__).parent / "input.txt") as city_f:
    for x, line in enumerate(city_f.readlines()):
        line = line.rstrip()
        row = [int(line[y]) for y in range(len(line))]
        city.append(row)

loss = find_path((0, 0), (len(city) - 1, len(city[0]) - 1), city, max_s=3)
print(f"Total loss (normal crucible): {loss}.")

loss = find_path((0, 0), (len(city) - 1, len(city[0]) - 1), city, max_s=10, min_s=4)
print(f"Total loss (ultra crucible): {loss}.")
