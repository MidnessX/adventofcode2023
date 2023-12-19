#!/usr/bin/env python3

from pathlib import Path

import numpy as np

directions: dict[str, tuple[int, int]] = {
    "R": (0, 1),
    "D": (1, 0),
    "L": (0, -1),
    "U": (-1, 0),
}


def decode_instruction(
    instruction: str, fix: bool = False
) -> tuple[int, tuple[int, int]]:
    d, count, color = instruction.rstrip().split(" ")

    if not fix:
        return int(count), directions.get(d)

    color = color[2:-1]

    d = int(color[-1])
    d = list(directions.keys())[
        d
    ]  # Dirty trick: since 0 = R, 1 = D, etc., we rely on the order of keys in the dict to look-up directions

    count = int(color[:5], 16)

    return count, directions[d]


def calculate_volume(x: np.ndarray, y: np.ndarray) -> float:
    # Shoelace formula to find the area of the pool.
    area = 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

    # From Pick's theorem we can derive the number of internal points.
    in_pts = area - (len(x) / 2) + 1

    return in_pts + len(x)


with open(Path(__file__).parent / "input.txt") as instr_f:
    x = [0]
    y = [0]

    for inst in instr_f.readlines():
        count, (dx, dy) = decode_instruction(inst, fix=False)

        for i in range(int(count)):
            x.append(x[-1] + dx)
            y.append(y[-1] + dy)

# The starting point has been added twice, so we remove its last occurrence.
x.pop()
y.pop()

x = np.asarray(x)
y = np.asarray(y)

volume = calculate_volume(x, y)
print(f"Pool volume: {volume}.")

with open(Path(__file__).parent / "input.txt") as instr_f:
    x = [0]
    y = [0]

    for inst in instr_f.readlines():
        count, (dx, dy) = decode_instruction(inst, fix=True)

        for i in range(int(count)):
            x.append(x[-1] + dx)
            y.append(y[-1] + dy)

# The starting point has been added twice, so we remove its last occurrence.
x.pop()
y.pop()

x = np.asarray(x)
y = np.asarray(y)

volume = calculate_volume(x, y)
print(f"Pool volume (with fixed instructions): {volume}.")
