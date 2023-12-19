#!/usr/bin/env python3

import heapq
from pathlib import Path


def get_neighbours(x, y, dx, dy, s, max_x, max_y) -> list[tuple[int, int]]:
    n = [(x - dy, y + dx), (x + dy, y - dx)]

    if s < 3:
        n.append([x + dx, y + dy])

    n = filter(lambda t: t[0] >= 0 and t[0] < max_x and t[1] >= 0 and t[1] < max_y, n)

    return n


def find_path(
    start: tuple[int, int], end: tuple[int, int], grid: list[list[int]]
) -> int:
    nodes = [(0, *start, 0, 1, 0)]
    visited = set()

    while nodes:
        c, x, y, dx, dy, s = heapq.heappop(nodes)

        if (x, y, dx, dy, s) in visited:
            continue

        visited.add((x, y, dx, dy, s))

        if (x, y) == end:
            return c

        for nx, ny in get_neighbours(x, y, dx, dy, s, len(grid), len(grid[0])):
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

loss = find_path((0, 0), (len(city) - 1, len(city[0]) - 1), city)

print(f"Total loss: {loss}.")
