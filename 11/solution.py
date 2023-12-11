from dataclasses import dataclass
from functools import reduce
from itertools import combinations
from pathlib import Path

# EXPANSION_COPIES = 1  # Part 1
EXPANSION_COPIES = int(1e6) - 1  # Part 2


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
            x += EXPANSION_COPIES

# Expand columns by adding the number of columns which have to be expanded that
# are found to the left of each galaxy, multiplied by the number of copies.
for galaxy in galaxies:
    dups = reduce(lambda x, y: x + y, cols_dup[: galaxy.y], False)
    galaxy.y += dups * EXPANSION_COPIES

total_distance = 0

for galaxy_a, galaxy_b in combinations(galaxies, 2):
    distance = abs(galaxy_a.x - galaxy_b.x) + abs(galaxy_a.y - galaxy_b.y)
    total_distance += distance

print(f"Total distance between pairs of galaxies: {total_distance}")
