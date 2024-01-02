#!/usr/bin/env python3

from pathlib import Path
from dataclasses import dataclass
from itertools import combinations

COLL_AREA_MIN = 200000000000000
COLL_AREA_MAX = 400000000000000


@dataclass
class Hail:
    x: int
    y: int
    z: int
    vx: int
    vy: int
    vz: int

    @property
    def slope_xy(self) -> float:
        # m = (y1 - y0) / (x1 - x0)
        # m = vy / vx

        return self.vy / self.vx

    @property
    def intercept_xy(self) -> float:
        # b = y - mx

        return self.y - (self.slope_xy * self.x)


def find_collisions(hail: list[Hail]) -> int:
    collisions = 0

    for hail_a, hail_b in combinations(hail, 2):
        if hail_a == hail_b:
            continue

        if hail_a.slope_xy == hail_b.slope_xy:
            # Parallel lines, they will never intercept
            continue

        x = (hail_b.intercept_xy - hail_a.intercept_xy) / (
            hail_a.slope_xy - hail_b.slope_xy
        )
        y = hail_a.slope_xy * x + hail_a.intercept_xy

        if (
            (x < hail_a.x and hail_a.vx > 0)
            or (x > hail_a.x and hail_a.vx < 0)
            or (x < hail_b.x and hail_b.vx > 0)
            or (x > hail_b.x and hail_b.vx < 0)
        ):
            # Interception point is in the past
            continue

        if COLL_AREA_MIN <= x <= COLL_AREA_MAX and COLL_AREA_MIN <= y <= COLL_AREA_MAX:
            collisions += 1

    return collisions


hail: list[Hail] = list()

with open(Path(__file__).parent / "input.txt") as hail_f:
    for line in hail_f.readlines():
        line = line.rstrip()

        pos, vel = line.split("@")

        x_pos, y_pos, z_pos = [int(p.replace(" ", "")) for p in pos.split(",")]
        x_vel, y_vel, z_vel = [int(v.replace(" ", "")) for v in vel.split(",")]

        hail.append(Hail(x_pos, y_pos, z_pos, x_vel, y_vel, z_vel))


collisions = find_collisions(hail)

print(f"Total collisions: {collisions}.")
