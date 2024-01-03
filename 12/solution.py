#!/usr/bin/env python3

import re
from functools import cache
from pathlib import Path

fault_re = re.compile(r"(#+)")


@cache
def compatible(line: str, counts: tuple[int, ...]) -> bool:
    faults = [len(group) for group in line.split(".")]
    return tuple(faults) == counts


@cache
def count_perms(line: str, faults: tuple[int, ...]) -> int:
    # If we don't have any more characters but the sequence of faults has not
    # been exhausted, it means character choices made so far lead to an
    # inadmissible sequence.
    if len(line) == 0 and len(faults) > 0:
        return 0

    # When our sequence of faults is empty, we may have found a valid sequence
    # of characters. This is true only when there are no more faults in the
    # line, otherwise we would need to have more faults for the sequence to be
    # valid.
    if len(faults) == 0:
        return 1 if "#" not in line else 0

    # When we are dealing with a . character we have nothing to do other than
    # checking the rest of the sequence.
    if line[0] in ".":
        return count_perms(line[1:], faults)

    # When we find a # character we must assume it to be part of sequence of
    # faulty springs having length given by the first entry of the faults tuple.
    # If the next character after this faulty sequence is not another #, and
    # simultaneously no . character was found in the sequence (i.e. it was a
    # real, contiguous sequence of faulty springs having the correct length),
    # then the string continues to be admissible and we can go on checking the
    # rest of it.
    # There's also a second, sneakier case: one where the sequence of faulty
    # spring reaches the end of the line. In this case we simply skip the check
    # on whether the next character after the fault differs from #, as we would
    # go out-of-bounds.
    # Another possible solution to this case would have been appending a . to
    # each line, making the check no longer necessary.
    # If neither of those two alternatives hold, it necessarily means the string
    # so far is not admissible.
    if line[0] == "#":
        if (
            faults[0] < len(line)
            and line[faults[0]] != "#"
            and "." not in line[: faults[0]]
        ):
            return count_perms(line[faults[0] + 1 :], faults[1:])
        elif faults[0] == len(line) and "." not in line:
            return count_perms("", faults[1:])
        else:
            return 0

    # line[0] == "?" here, so we simply have to swap it with each of the two
    # possible alternatives and sum together the possible permutations for each
    # case.
    return sum(count_perms(alt + line[1:], faults) for alt in ".#")


poss = 0
poss_unrolled = 0

with open(Path(__file__).parent / "input.txt") as diag_f:
    for line in diag_f.readlines():
        chars, counts = line.split(" ")
        counts = tuple([int(c) for c in counts.split(",")])

        poss += count_perms(chars, counts)
        poss_unrolled += count_perms("?".join([chars] * 5), counts * 5)

print(f"Total possibilities: {poss}.")
print(f"Total possibilities (unrolled): {poss_unrolled}.")
