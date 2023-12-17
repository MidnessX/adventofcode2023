#!/usr/bin/env python3

from pathlib import Path
import numpy as np
from dataclasses import dataclass
from enum import Enum


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
    while True:
        if x < 0 or x >= contr.shape[0] or y < 0 or y >= contr.shape[1]:
            return

        prev = energized_tiles.get((x, y))

        if prev:
            for vis_dir in prev:
                if vis_dir == direction:
                    return
            prev.append(direction)
        else:
            energized_tiles[(x, y)] = [direction]

        elem = contr[x, y]

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

print(f"Energized nodes: {len(energ.keys())}")
