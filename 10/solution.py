#!/usr/bin/env python3

from pathlib import Path
import sys
from dataclasses import dataclass

sys.setrecursionlimit(10000)

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
        if e_pipe == prev:
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

path = navigate(start, start, pipes)
print(f"Steps to reach farthest point in loop: {len(path) // 2}")
