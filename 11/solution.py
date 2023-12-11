from dataclasses import dataclass
from functools import reduce
from itertools import combinations
from pathlib import Path


@dataclass
class Galaxy:
    x: int
    y: int


galaxies = list()

with open(Path(__file__).parent / "input.txt") as map_f:
    x = 0
    cols_dup = None

    for line in map_f.readlines():
        line = line.rstrip()

        if not cols_dup:
            cols_dup = [1] * len(line)

        has_galaxy = False

        for y, char in enumerate(line):
            if char == "#":
                galaxies.append(Galaxy(x, y))
                has_galaxy = True
                cols_dup[y] = 0

        x += 1

        if not has_galaxy:
            x += 1

for galaxy in galaxies:
    dups = reduce(lambda x, y: x + y, cols_dup[: galaxy.y], False)
    galaxy.y += dups

total_distance = 0

for galaxy_a, galaxy_b in combinations(galaxies, 2):
    distance = abs(galaxy_a.x - galaxy_b.x) + abs(galaxy_a.y - galaxy_b.y)
    total_distance += distance

print(f"Total distance between pairs of galaxies: {total_distance}")
