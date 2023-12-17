#!/usr/bin/env python3

from pathlib import Path
import numpy as np
from dataclasses import dataclass


@dataclass
class Direction:
    deg: int
    tup: tuple[int, int]

    def rot_clkws(self) -> "Direction":
        deg = (self.deg + 90) % 360

        return Direction(deg, (self.tup[1], -self.tup[0]))

    def rot_cclkws(self) -> "Direction":
        deg = (self.deg - 90) % 360

        return Direction(deg, (-self.tup[1], self.tup[0]))

    def __eq__(self, other) -> bool:
        if not isinstance(other, Direction):
            return False

        return self.deg == other.deg


def navigate(
    contr: np.ndarray,
    energized_tiles: dict[tuple[int, int], list[Direction]],
    x: int,
    y: int,
    direction: Direction,
) -> None:
    # The trick here is to remember which tiles have already been energized by
    # a beam, since loops can be formed.
    # We use the variable energized_tiles for this purpose, which maps a tile
    # (given by its coordinates) to a list of directions along which a beam
    # has already travelled.

    # We could use a fully recursive function, but to save stack space we march
    # the beam until we have to split it.
    while True:
        if x < 0 or x >= contr.shape[0] or y < 0 or y >= contr.shape[1]:
            return

        prev = energized_tiles.get((x, y))

        # If the current tile has already been energized, check if it happened
        # due to a beam travelling in the same direction as the one we currently
        # are following. If that's the case, a loop has been formed and we can
        # stop.
        if prev:
            for vis_dir in prev:
                if vis_dir == direction:
                    return
            # The tile was energized, but not by a beam in the same direction.
            # Add this new direction to the list and continue.
            prev.append(direction)
        else:
            # Mark the tile as energized by storing the direction.
            energized_tiles[(x, y)] = [direction]

        elem = contr[x, y]

        # Mirrors make a beam rotate 90 degrees either clockwise or counter
        # clockwise depending on the orientation of both the beam and the
        # mirror. There are always two opposite directions where the beam
        # is rotated in the same way for each mirror type, and two more where
        # the beam is rotated in the opposite way.
        if elem == "/":
            if direction.deg == 0 or direction.deg == 180:
                direction = direction.rot_clkws()
            else:
                direction = direction.rot_cclkws()
        elif elem == "\\":
            if direction.deg == 0 or direction.deg == 180:
                direction = direction.rot_cclkws()
            else:
                direction = direction.rot_clkws()
        elif elem == "|":
            if direction.deg == 90 or direction.deg == 270:
                navigate(
                    contr,
                    energized_tiles,
                    x + direction.rot_clkws().tup[0],
                    y + direction.rot_clkws().tup[1],
                    direction.rot_clkws(),
                )
                navigate(
                    contr,
                    energized_tiles,
                    x + direction.rot_cclkws().tup[0],
                    y + direction.rot_cclkws().tup[1],
                    direction.rot_cclkws(),
                )
                return
        elif elem == "-":
            if direction.deg == 0 or direction.deg == 180:
                navigate(
                    contr,
                    energized_tiles,
                    x + direction.rot_clkws().tup[0],
                    y + direction.rot_clkws().tup[1],
                    direction.rot_clkws(),
                )
                navigate(
                    contr,
                    energized_tiles,
                    x + direction.rot_cclkws().tup[0],
                    y + direction.rot_cclkws().tup[1],
                    direction.rot_cclkws(),
                )
                return

        x += direction.tup[0]
        y += direction.tup[1]


with open(Path(__file__).parent / "input.txt") as contr_f:
    contr = [list(line.rstrip()) for line in contr_f.readlines()]

contr = np.asarray(contr)
energ = dict()
navigate(contr, energ, 0, 0, direction=Direction(90, (0, 1)))

print(f"Energized nodes: {len(energ.keys())}.")

max_energ = 0

for i in range(contr.shape[0]):
    for j, direction in [
        (0, Direction(90, (0, 1))),
        (contr.shape[1] - 1, Direction(270, (0, -1))),
    ]:
        energ = dict()
        navigate(contr, energ, i, j, direction)

        if len(energ.keys()) > max_energ:
            max_energ = len(energ.keys())
        # max_energ = max(max_energ, len(energ.keys()))
for j in range(contr.shape[1]):
    for i, direction in [
        (0, Direction(180, (1, 0))),
        (contr.shape[0] - 1, Direction(0, (-1, 0))),
    ]:
        energ = dict()
        navigate(contr, energ, i, j, direction)

        if len(energ.keys()) > max_energ:
            max_energ = len(energ.keys())
        # max_energ = max(max_energ, len(energ.keys()))

print(f"Maximum energized nodes: {max_energ}.")
