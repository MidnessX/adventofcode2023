#!/usr/bin/env python3

# I have no idea why counts for part 2 are considered too high (36506), as all
# the reflections found by the code appear to respect the criteria (only one
# possible character substitution).
# Comparing results with another script giving the right answer (31603), it
# appears that this second script misses vertical reflections found by my code.

from enum import IntEnum, auto
from pathlib import Path

import numpy as np

FIX_SMUDGES = True


class Directions(IntEnum):
    H = auto()
    V = auto()


def find_reflections(pattern: np.ndarray, fix: bool = False) -> tuple[int, Directions]:
    # Horizontal reflection
    for i in range(pattern.shape[0] - 1):
        valid = True
        # If we don't want to allow any character substitution as in part 1,
        # we simply have to set fixed to True.
        fixed = False if fix else True

        for j in range(min(pattern.shape[0] - i - 1, i + 1)):
            diff = pattern[i - j] != pattern[i + j + 1]

            # If there's no difference, continue
            if not any(diff):
                continue

            # If differences are greater than 1, or we already fixed a
            # smudge, there's nothing else we can do
            if fixed or sum(diff) > 1:
                valid = False
                break

            # Mark that we had to swap a symbol due to a smudge in the pattern
            fixed = True

        if valid:
            return (i + 1, Directions.H)

    # Vertical reflection
    for i in range(pattern.shape[1] - 1):
        valid = True
        fixed = False if fix else True

        for j in range(min(pattern.shape[1] - i - 1, i + 1)):
            diff = pattern[:, i - j] != pattern[:, i + j + 1]

            if not any(diff):
                continue

            if fixed or sum(diff) > 1:
                valid = False
                break

            fixed = True

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

        i, direction = find_reflections(np.array(pattern), fix=FIX_SMUDGES)
        summary += summarize(i, direction)

        pattern.clear()

    i, direction = find_reflections(np.array(pattern), fix=FIX_SMUDGES)
    summary += summarize(i, direction)

print(
    f"Reflection summary ({'smudges fixed' if FIX_SMUDGES else 'smudges not fixed'}): {summary}"
)
