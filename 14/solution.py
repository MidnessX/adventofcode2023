#!/usr/bin/env python3

from pathlib import Path


def tilt_north(platform: list[list[str]]) -> None:
    empty_pos = [0] * len(platform)

    for i, row in enumerate(platform):
        for j, item in enumerate(row):
            if item == "#":
                empty_pos[j] = i + 1
            if item == "O":
                platform[empty_pos[j]][j] = "O"
                if empty_pos[j] != i:
                    platform[i][j] = "."

                empty_pos[j] += 1


def weight(platform: list[str]) -> int:
    total_weight = 0

    for i, row in enumerate(platform):
        for item in row:
            if item == "O":
                total_weight += len(platform) - i

    return total_weight


with open(Path(__file__).parent / "input.txt") as pltf_f:
    pltf = [list(line.rstrip()) for line in pltf_f.readlines()]

tilt_north(pltf)
total_load = weight(pltf)

print(f"Total platform load: {total_load}")
