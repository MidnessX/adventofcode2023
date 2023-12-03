#!/usr/bin/env python3

# This solution assumes the following:
#   1. A part number can only have a single adjacent symbol.
#   2. A part symbol is any character other than a dot, a newline or a digit.

import re
from dataclasses import dataclass


@dataclass
class PartNumber:
    value: int
    symbol: str | None = None
    row: int | None = None
    col: int | None = None


def is_valid(
    start_pos: int,
    end_pos: int,
    line: str,
    prev_line: str | None,
    next_line: str | None,
    line_no: int,
    operators=set[str],
) -> PartNumber:
    value = int(line[start_pos : end_pos + 1])
    symbol = None
    row = None
    col = None

    l = start_pos - 1 if start_pos > 0 else start_pos
    r = end_pos + 1 if end_pos < len(line) - 1 else end_pos

    for i in range(l, r + 1):
        if prev_line is not None and prev_line[i] in operators:
            symbol = prev_line[i]
            row = line_no - 1
            col = i
        if line[i] in operators:
            symbol = line[i]
            row = line_no
            col = i
        if next_line is not None and next_line[i] in operators:
            symbol = next_line[i]
            row = line_no + 1
            col = i

    return PartNumber(value, symbol, row, col)


number_re = re.compile(r"(\d+)")

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
    gear_ratio_sum = 0

    prev_line = None
    line = schematic_f.readline()
    next = schematic_f.readline()
    next_line = next if next != "" else None

    line_no = 0

    possible_gears: dict[tuple[int, int], PartNumber] = dict()

    while line is not None:
        for match in number_re.finditer(line):
            part = is_valid(
                match.start(),
                match.end() - 1,
                line,
                prev_line,
                next_line,
                line_no,
                operators,
            )

            if part.symbol is not None:
                value_sum += int(match.group())

                if part.symbol == "*":
                    other_gear = possible_gears.pop((part.row, part.col), None)

                    if other_gear is not None:
                        gear_ratio_sum += other_gear.value * part.value
                    else:
                        possible_gears[(part.row, part.col)] = part

        prev_line = line
        line = next_line
        next = schematic_f.readline()
        next_line = next if next != "" else None

        line_no += 1

    print(f"Sum of valid part numbers: {value_sum}")
    print(f"Sum of gear ratios: {gear_ratio_sum}")
