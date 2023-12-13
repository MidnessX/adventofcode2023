#!/usr/bin/env python3

from enum import IntEnum, auto
from pathlib import Path

import numpy as np


class Directions(IntEnum):
    H = auto()
    V = auto()


def find_reflections(pattern: np.ndarray[str]) -> tuple[int, Directions]:
    # Horizontal reflection
    for i in range(0, pattern.shape[0] - 1):
        if all(pattern[i] == pattern[i + 1]):
            valid = True

            # Check each pair of rows starting from i and moving farther away.
            # We do this for a number of times equal to the minimum between
            # i (i.e. the number of rows above) and pattern.shape[0] - i (i.e.
            # the number of rows below).
            # We add 1 to i since the range starts at 1 (the row before) and we
            # subtract 1 to pattern.shape[0] - i due to having to skip the
            # i+1-th row that we already checked.
            for j in range(1, min(pattern.shape[0] - i - 1, i + 1)):
                if any(pattern[i - j] != pattern[i + j + 1]):
                    valid = False
                    break

            if valid:
                return (i + 1, Directions.H)

    # Vertical reflection
    # Same as for rows, only checking columns this time.
    for i in range(0, pattern.shape[1] - 1):
        if all(pattern[:, i] == pattern[:, i + 1]):
            valid = True

            for j in range(1, min(pattern.shape[1] - i - 1, i + 1)):
                if any(pattern[:, i - j] != pattern[:, i + j + 1]):
                    valid = False
                    break

            if valid:
                return (i + 1, Directions.V)

    raise ValueError("No reflection found in pattern.")


def summarize(r_position: int, direction: Directions) -> int:
    if direction == Directions.V:
        return r_position
    else:
        return 100 * r_position


with open(Path(__file__).parent / "input.txt") as pat_f:
    pattern = list()
    summary = 0

    for line in pat_f.readlines():
        line = line.rstrip()
        if line != "":
            pattern.append([char for char in line])
            continue

        i, direction = find_reflections(np.array(pattern))
        summary += summarize(i, direction)

        pattern.clear()

    i, direction = find_reflections(np.array(pattern))
    summary += summarize(i, direction)

print(f"Reflection summary: {summary}")
