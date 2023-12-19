#!/usr/bin/env python3

import math
from bisect import bisect_left, bisect_right, insort_right
from dataclasses import dataclass
from functools import total_ordering
from pathlib import Path

import numpy as np


@total_ordering
@dataclass
class Block:
    x: int
    y: int
    loss: int
    cost: float = math.inf
    est_cost: float = math.inf
    came_from: tuple[int, int] = None
    dir_count: int = 0

    def neighbors(self) -> list[tuple[int, int]]:
        l = [
            (self.x + self.dir_diff[1], self.y - self.dir_diff[0]),
            (self.x - self.dir_diff[1], self.y + self.dir_diff[0]),
        ]

        if self.dir_count < 3:
            l.insert(0, (self.x + self.dir_diff[0], self.y + self.dir_diff[1]))

        l = list(
            filter(
                lambda t: t[0] >= 0
                and t[0] < len(city)
                and t[1] >= 0
                and t[1] < len(city[0]),
                l,
            )
        )

        return l

    @property
    def as_tuple(self) -> tuple[int, int]:
        return (self.x, self.y)

    @property
    def dir_diff(self) -> tuple[int, int]:
        return (self.x - self.came_from[0], self.y - self.came_from[1])

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Block):
            return False

        return self.est_cost == __value.est_cost

    def __gt__(self, __value: object) -> bool:
        if not isinstance(__value, Block):
            raise NotImplementedError()

        return self.est_cost > __value.est_cost


def path_cost(end: tuple[int, int]) -> int:
    cost = 0

    n = city[end[0]][end[1]]

    m = np.full((len(city), len(city[0])), ".")

    while n.as_tuple != (0, 0):
        cost += n.loss
        m[n.x, n.y] = "#"
        n = city[n.came_from[0]][n.came_from[1]]

    print(m)

    return cost


def a_star(start: tuple[int, int], end: tuple[int, int], heur_f) -> int:
    s = city[start[0]][start[1]]
    s.cost = 0
    s.est_cost = heur_f(s.as_tuple, end)
    s.came_from = (0, -1)

    nodes = [s]

    while len(nodes) > 0:
        current = nodes.pop(0)

        if current.as_tuple == end:
            return path_cost(current.as_tuple)

        for n_x, n_y in current.neighbors():
            n = city[n_x][n_y]

            new_cost = current.cost + n.loss

            if new_cost < n.cost:
                found = False

                # Can't use x in nodes due to the way __eq__() is implemented.
                for i, x in enumerate(nodes):
                    if x.as_tuple == n.as_tuple:
                        found = True
                        break

                if found:
                    nodes.pop(i)

                n.came_from = current.as_tuple
                n.dir_count = (
                    current.dir_count + 1 if current.dir_diff == n.dir_diff else 1
                )
                n.cost = new_cost
                n.est_cost = new_cost + heur_f(n.as_tuple, end)

                insort_right(nodes, n)


city: list[list[Block]] = list()

with open(Path(__file__).parent / "input.txt") as city_f:
    for x, line in enumerate(city_f.readlines()):
        line = line.rstrip()
        row = [Block(x, y, int(line[y])) for y in range(len(line))]
        city.append(row)

loss = a_star(
    (0, 0),
    (len(city) - 1, len(city[0]) - 1),
    lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1]),
)

print(f"Total loss: {loss}.")
