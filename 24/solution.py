#!/usr/bin/env python3

from pathlib import Path
from dataclasses import dataclass
from itertools import combinations
import numpy as np

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

    def as_ndarray(self) -> tuple[np.ndarray, np.ndarray]:
        # Use float64 as the default int64 leads to overflow in some operations
        # such as the dot product.
        pos = np.asarray((self.x, self.y, self.z), dtype=np.float64)
        vel = np.asarray((self.vx, self.vy, self.vz), dtype=np.float64)

        return pos, vel


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


def are_independent(a: np.ndarray, b: np.ndarray) -> bool:
    # a and b are linearly dependent iff a x b = 0

    cp = np.cross(a, b)

    return np.any(cp)


def find_independent_hailstones(hail: list[Hail]) -> list[Hail]:
    indep = [hail[0]]

    start = 1
    while len(indep) != 3:
        if start >= len(hail):
            raise ValueError("Could not find enough 3 independent hailstones.")

        for i in range(start, len(hail)):
            candidate = hail[i]

            if all(
                map(
                    lambda h: are_independent(
                        h.as_ndarray()[1], candidate.as_ndarray()[1]
                    ),
                    indep,
                )
            ):
                indep.append(candidate)
                break

        start = i

    return indep


def find_plane(hail_a: Hail, hail_b: Hail) -> tuple[np.ndarray, int]:
    pa, va = hail_a.as_ndarray()
    pb, vb = hail_b.as_ndarray()

    pab = pa - pb
    vab = va - vb

    a = np.cross(pab, vab)
    A = np.dot(pab, np.cross(va, vb))

    return a, A


def find_velocity_adj(planes: list[tuple[np.ndarray, int]]) -> np.ndarray:
    a, A = planes[0]
    b, B = planes[1]
    c, C = planes[2]

    if not (are_independent(a, b) and are_independent(b, c) and are_independent(a, c)):
        raise ValueError(f"a, b, and c are not independent.")

    w = np.dot(
        np.stack([np.cross(b, c), np.cross(c, a), np.cross(a, b)], axis=1),
        np.asarray((A, B, C)),
    )
    t = np.dot(a, np.cross(b, c))

    w = (w / t).astype(int)

    return w


def rock_staring_point(hail: list[Hail]) -> np.ndarray:
    """
    This solution directly follows the explanation given in
    https://www.reddit.com/r/adventofcode/comments/18pnycy/2023_day_24_solutions/kersplf/
    I honestly would not have been able to find it on my own and probably ended
    up using a solver instead.

    The existance of a solution to this problem (a rock position and velocity
    allowing it to hit all the hailstones) cannot be assumed in a truly random
    setting, so it means that, for this particular set of hailstones, a solution
    exists and can be found by only considering three hailstones having
    independent velocities.

    Let's start by observing that a rock, starting at position r and having
    velocity w, hitting a hailstone i at time t means:
    r + t*w = pi + vi*t
    Which can be rewritten as:
    r = pi + (vi - w)*t

    This tells us that adjusting hailstone velocities by -w (a constant) makes
    them pass through a single common point.

    As said before, we have three independent lines (hailston trajectories)
    which we call (p1, v1), (p2, v2) and (p3, v3).
    A necessary and sufficient condition for any two of them to have a common
    intersection point is that (pa - pb) . (va x vb) = 0.
    Recalling that we are applying an adjustment to each velocity, this
    translates into (for the first pair):
    (p1 - p2) . [(v1 - w) x (v2 - w)]

    Expanding and shifting around this equation we get:
    (p1 - p2) . (v1 x v2) = (p1 - p2) . [(v1 - v2) x w]

    The term on the left is completely made up of known terms, so we call it M.
    M = (p1 - p2) . [(v1 - v2) x w]

    Using the definition of scalar triple product
    https://en.wikipedia.org/wiki/Triple_product#Scalar_triple_product
    we can turn the equation into:
    M = w . [(p1 - p2) x (v1 - v2)]
    which is an equation of the form w . a = A (i.e. a plane, since we want M
    to be 0 in order to have a common intersection point.

    Now, the point where the rock is initially located is the point given by
    the intersection of three such planes.
    We repeat the same operation for all the combinations of the three
    linearly independent hailstones, giving us:
    w . a = A (p1, p2)
    w . b = B (p1, p3)
    w . c = C (p2, p3)

    If a, b, and c are independent, we can write  w as:
    w = p * (b x c) + q * (c x a) + r * (a x b)

    Putting this into the three plane equations gives us:
    A = w . a = p * a . (b x c)
    B = w . b = q * b . (c x a)
    C = w . c = r * c . (a x b)

    Solving for p, q, and r allows us to find w (i.e. our velocity adjustment).
    In order to prevent floating point errors (since we have to divide by
    a * (b x c)), we cast w components to integers.

    Finally, we can apply this velocity adjustment to two hailstones and find
    their intersection point, which will be the starting position of the rock
    (basically part 1 of the problem, but in 3D space).
    """

    ind_hailstones = find_independent_hailstones(hail)

    planes = [find_plane(h1, h2) for h1, h2 in combinations(ind_hailstones, 2)]

    adj_vel = find_velocity_adj(planes)

    pa, va = ind_hailstones[0].as_ndarray()
    pb, vb = ind_hailstones[1].as_ndarray()

    va = va - adj_vel
    vb = vb - adj_vel

    # Find the intersection point between hailston a and b.
    i = np.dot(
        np.cross(va, vb),
        np.cross(pb, vb),
    )
    j = np.dot(np.cross(va, vb), np.cross(pa, va))
    k = np.dot(pa, np.cross(va, vb))

    scale = np.dot(np.cross(va, vb), np.cross(va, vb))

    starting_point = np.dot(
        np.stack([va, vb, np.cross(va, vb)], axis=1), np.asarray([i, -j, k])
    )
    starting_point = starting_point / scale

    return starting_point


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

rock = rock_staring_point(hail)
print(f"Sum of rock's coordinates: {int(sum(rock))}.")
