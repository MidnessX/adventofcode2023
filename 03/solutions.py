#!/usr/bin/env python3

import re

number_re = re.compile(r"(\d+)")


def is_valid(
    start_pos: int,
    end_pos: int,
    line: str,
    prev_line: str | None,
    next_line: str | None,
    operators=set[str],
) -> bool:
    valid = False

    l = start_pos - 1 if start_pos > 0 else start_pos
    r = end_pos + 1 if end_pos < len(line) - 1 else end_pos

    for i in range(l, r + 1):
        if prev_line is not None and prev_line[i] in operators:
            valid = True
            break
        if line[i] in operators:
            valid = True
            break
        if next_line is not None and next_line[i] in operators:
            valid = True
            break

    return valid


operators = set()

# Read the whole file one to get all the possible operator characters.
with open("03/input.txt") as schematic_f:
    c = schematic_f.read(1)

    while c != "":
        if c != "." and not c.isnumeric() and c != "\n":
            operators.add(c)

        c = schematic_f.read(1)


with open("03/input.txt") as schematic_f:
    value_sum = 0
    prev_line = None
    line = schematic_f.readline()
    next = schematic_f.readline()
    next_line = next if next != "" else None

    while line is not None:
        for match in number_re.finditer(line):
            if is_valid(
                match.start(), match.end() - 1, line, prev_line, next_line, operators
            ):
                value_sum += int(match.group())

        prev_line = line
        line = next_line
        next = schematic_f.readline()
        next_line = next if next != "" else None

    print(f"Sum of valid part numbers: {value_sum}")
