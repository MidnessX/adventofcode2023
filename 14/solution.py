#!/usr/bin/env python3

from pathlib import Path


with open(Path(__file__).parent / "input.txt") as pltf_f:
    length = len(pltf_f.readline().rstrip())
    pltf_f.seek(0)
    rows = len(pltf_f.readlines())
    pltf_f.seek(0)

    empty_pos = [-1] * length
    total_load = 0

    for i, line in enumerate(pltf_f.readlines()):
        line = line.rstrip()

        for j, item in enumerate(line):
            if item == "#":
                empty_pos[j] = i
            if item == "O":
                empty_pos[j] += 1
                total_load += rows - empty_pos[j]

print(f"Total platform load: {total_load}")
