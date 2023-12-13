#!/usr/bin/env python3

import re
from functools import lru_cache
from pathlib import Path

fault_re = re.compile(r"(#+)")


@lru_cache(maxsize=None)
def get_faults(line: str) -> tuple[int, ...]:
    f_found = tuple([len(m.group()) for m in fault_re.finditer(line)])

    return f_found


@lru_cache(maxsize=None)
def permutations(line: str) -> tuple[str, ...]:
    if len(line) == 1:
        if line[0] == "?":
            return (".", "#")
        return line

    perms = list()

    if line[0] == "?":
        for subst in [".", "#"]:
            perms.extend([subst + p for p in permutations(line[1:])])
    else:
        perms.extend([line[0] + p for p in permutations(line[1:])])

    return tuple(perms)


poss = 0

with open(Path(__file__).parent / "input.txt") as diag_f:
    for line in diag_f.readlines():
        chars, counts = line.split(" ")
        counts = tuple([int(c) for c in counts.split(",")])

        for p in permutations(chars):
            if len(p) != len(chars):
                raise ValueError()

            if get_faults(p) == counts:
                poss += 1

print(f"Total possibilities: {poss}.")
