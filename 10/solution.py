#!/usr/bin/env python3

from pathlib import Path
from dataclasses import dataclass

# X are rows in the map.
# Y are columns in the map.


@dataclass
class Pipe:
    x: int
    y: int
    entrypoints: list[tuple[int, int]]
    type: str

    @classmethod
    def from_char(cls, x: int, y: int, char: str) -> "Pipe":
        if char == "|":
            return Pipe(x, y, entrypoints=[(-1, 0), (1, 0)], type=char)
        if char == "-":
            return Pipe(x, y, entrypoints=[(0, -1), (0, 1)], type=char)
        if char == "L":
            return Pipe(x, y, entrypoints=[(-1, 0), (0, 1)], type=char)
        if char == "J":
            return Pipe(x, y, entrypoints=[(-1, 0), (0, -1)], type=char)
        if char == "7":
            return Pipe(x, y, entrypoints=[(0, -1), (1, 0)], type=char)
        if char == "F":
            return Pipe(x, y, entrypoints=[(0, 1), (1, 0)], type=char)
        if char == ".":
            return Pipe(x, y, entrypoints=[], type=char)
        if char == "S":
            return Pipe(x, y, entrypoints=[(-1, 0), (0, 1), (1, 0), (0, -1)], type=char)

        raise ValueError(f"Unsupported characted {char}")

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Pipe):
            return False

        return self.x == __value.x and self.y == __value.y

    def __repr__(self) -> str:
        return f"{self.type} ({self.x}, {self.y})"


def navigate_recursive(
    pipe: Pipe,
    prev: Pipe | None,
    start: Pipe,
    pipes: list[list[Pipe]],
) -> list[Pipe]:
    # Does not work on input.txt due to the path being too long and causing a
    # stack overflow.

    if prev and pipe == start:
        return [pipe]

    for entrypoint in pipe.entrypoints:
        e_x = pipe.x + entrypoint[0]
        e_y = pipe.y + entrypoint[1]

        # Check that we are not exceeding map boundaries
        if e_x < 0 or e_x >= len(pipes) or e_y < 0 or e_y >= len(pipes[pipe.x]):
            continue

        e_pipe = pipes[e_x][e_y]

        # Check that we are not going back to the previous pipe
        if prev and e_pipe == prev:
            continue

        other_ep = list(
            map(lambda ep: (e_pipe.x + ep[0], e_pipe.y + ep[1]), e_pipe.entrypoints)
        )

        # Check that the pipe at the entrypoint is compatible with this pipe
        if not (pipe.x, pipe.y) in other_ep:
            continue

        path = navigate_recursive(e_pipe, pipe, start, pipes)
        path.insert(0, pipe)

        return path

    raise ValueError("No loop exists")


def navigate(pipe: Pipe, start: Pipe, pipes: list[list[Pipe]]) -> list[Pipe]:
    path = list()

    while pipe != start or len(path) == 0:
        for entrypoint in pipe.entrypoints:
            e_x = pipe.x + entrypoint[0]
            e_y = pipe.y + entrypoint[1]

            # Check that we are not exceeding map boundaries
            if e_x < 0 or e_x >= len(pipes) or e_y < 0 or e_y >= len(pipes[pipe.x]):
                continue

            e_pipe = pipes[e_x][e_y]

            # Check that we are not going back to the previous pipe
            if len(path) > 0 and e_pipe == path[-1]:
                continue

            other_ep = list(
                map(lambda ep: (e_pipe.x + ep[0], e_pipe.y + ep[1]), e_pipe.entrypoints)
            )

            # Check that the pipe at the entrypoint is compatible with this pipe
            if not (pipe.x, pipe.y) in other_ep:
                continue

            path.append(pipe)

            pipe = e_pipe
            break

    return path


def substitute_start(start: Pipe, prev: Pipe, next: Pipe) -> None:
    candidates = set(["|", "L", "J", "7", "F", "-"])

    for comp in [prev, next]:
        if comp.x == start.x:
            candidates -= set(["|"])
        elif comp.x == start.x - 1:
            candidates -= set(["7", "F", "-"])
        else:
            candidates -= set(["L", "J", "-"])

        if comp.y == start.y:
            candidates -= set(["-"])
        elif comp.y == start.y - 1:
            candidates -= set(["|", "L", "F"])
        else:
            candidates -= set(["|", "J", "7"])

    if len(candidates) > 1:
        raise ValueError("More than one possibilities left.")

    return candidates.pop()


def count_inside(
    pipes: list[list[Pipe]], loop: list[Pipe], boundaries: tuple[int, int, int, int]
) -> int:
    x_min, y_min, x_max, y_max = boundaries

    tiles_inside = 0

    for i in range(x_min, x_max):
        inside = False

        for j in range(y_min, y_max):
            tile = pipes[i][j]

            if tile in loop:
                if tile.type in ["|", "L", "J"]:
                    inside = not inside
                continue

            if inside:
                tiles_inside += 1

    return tiles_inside


pipes = list()
start = None

with open(Path(__file__).parent / "input.txt") as map_f:
    x = 0

    for line in map_f.readlines():
        line = line.rstrip()

        line_pipes = [Pipe.from_char(x, y, line[y]) for y in range(len(line))]

        # Search for the starting position
        for pipe in line_pipes:
            if len(pipe.entrypoints) == 4:
                start = pipe

        pipes.append(line_pipes)

        x += 1

# Part 1

# path = navigate_recursive(start, None, start, pipes)
path = navigate(start, start, pipes)

print(f"Steps to reach farthest point in loop: {len(path) // 2}")

# Part 2
# If we assume the loop to have a direction (e.g. clockwise), a tile will be
# inside the loop if it's found to the right of the loop tile.
# This allows us to count the number of loop tiles encountered to the left of
# a tile to determine whether or not it is inside the loop (i.e. even = outside,
# odd = inside).
# More precisely, since we are dealing with a grid, we can restrict our
# calculations to just one dimension. We chose the X axis (i.e. rows) for
# simplicity.
# This allows us to only consider loop pipes of type |, L, or J, as those are
# ones indicating a change of direction in the loop along the row.
#
# e.g.
# |..|.||
# means that the first pipe on the left was travelled bottom-up, the second pipe
# top-down. the third bottom-up and the fourht bottom-up again.
# The first two . are thus inside the loop, while the third . is outside.
#
# e.g.
# F-7.F-7
# |.|.|.|
# # means that, on the first row, the only . is outside, while on the second row
# # the first and the third . are inside and the second one is outside.
#
# The only caveat is with the starting node, S, which must be transformed into
# the real type for this approach to work correctly.
substitute_start(start, path[-1], path[1])

x_min = min(path, key=lambda pipe: pipe.x)
x_max = max(path, key=lambda pipe: pipe.x)
y_min = min(path, key=lambda pipe: pipe.y)
y_max = max(path, key=lambda pipe: pipe.y)

tiles_inside = count_inside(pipes, path, (x_min.x, y_min.y, x_max.x + 1, y_max.y + 1))

print(f"Tiles inside the loop: {tiles_inside}")
