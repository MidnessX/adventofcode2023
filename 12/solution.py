#!/usr/bin/env python3

import re
from pathlib import Path

fault_re = re.compile(r"(#+)")


def is_possible(line: str, faults: list[int], unkw_n: int) -> bool:
    # The logic of this function can be further refined to identify impossible
    # substitutions earlier on, but it is an error-prone task.
    # We chose to trade speed for simplicity and mark a sequence as incompatible
    # only when no more substitutions are possible and there's a mismatch
    # between the number of faults and the faults found in the sequence.

    if unkw_n != 0:
        return True

    f_found = [len(m.group()) for m in fault_re.finditer(line)]

    if len(f_found) == len(faults) and f_found == faults:
        return True

    return False


def permutations(line: str, pos: int, counts: list[int]) -> list[str]:
    if pos == len(line):
        if is_possible(line, counts, 0):
            return [line]
        return list()

    if line[pos] != "?":
        return permutations(line, pos + 1, counts)

    res = list()

    for subst in [".", "#"]:
        line = line[: max(0, pos)] + subst + line[min(pos + 1, len(line)) :]
        unkw_n = (
            sum(map(lambda c: c == "?", line[pos + 1 :])) if pos < len(line) - 1 else 0
        )

        if not is_possible(line, counts, unkw_n):
            continue

        x = permutations(line, pos + 1, counts)
        res.extend(x)

    return res


poss = list()

with open(Path(__file__).parent / "input.txt") as diag_f:
    for line in diag_f.readlines():
        chars, counts = line.split(" ")
        counts = [int(c) for c in counts.split(",")]

        poss.extend(permutations(chars, 0, counts))

print(f"Total possibilities: {len(poss)}.")
