#!/usr/bin/env python3

from pathlib import Path
import numpy as np


def tilt(platform: np.ndarray) -> None:
    empty_pos = [0] * platform.shape[0]

    for i in range(platform.shape[0]):
        for j, item in enumerate(platform[i, :]):
            if item == "#":
                empty_pos[j] = i + 1
            if item == "O":
                platform[empty_pos[j]][j] = "O"
                if empty_pos[j] != i:
                    platform[i][j] = "."

                empty_pos[j] = empty_pos[j] + 1


def weight(platform: np.ndarray) -> int:
    total_weight = 0

    for i, row in enumerate(platform):
        for item in row:
            if item == "O":
                total_weight += len(platform) - i

    return total_weight


with open(Path(__file__).parent / "input.txt") as pltf_f:
    pltf = np.asarray(
        [tuple(line.rstrip()) for line in pltf_f.readlines()], dtype=np.str_
    )

print("Part 1.")
tilt(pltf)
print(f"Total platform load: {weight(pltf)}")

print("Part 2.")
prev_pltf = list()
cycle = -1
i = 0

while i < 1000000000:
    for _ in range(4):
        tilt(pltf)
        # We don't need to define four different tilt functions.
        # We can, instead, rotate the matrix clockwise and obtain the same
        # result.
        pltf = np.rot90(pltf, axes=(1, 0))  # axes=(1,0) means clockwise

    if cycle == -1:
        prev_pltf.append(pltf.copy())

        for j, pp in enumerate(prev_pltf):
            if j == i:
                continue

            if np.all(pp == pltf):
                cycle = i - j
                print(f"Found cycle starting from iteration {i}: length {cycle}")
                i += ((1000000000 - i) // cycle) * cycle
                print(f"Skipping to iteration {i}")
                break

    i += 1

print(f"Total platform load (after 1000000000 cycles): {weight(pltf)}")
