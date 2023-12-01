#!/usr/bin/env python3

# I use regex instead of the built-in re as it supports overlapping matches,
# which is needed since some rows in the input file have overlapping strings.
# e.g. xtwone3four has to be interpreted as x2134.
#
# A finite-state machine would be more efficient, but I could not find any
# pre-made library simple enough for the task.

import regex as re

DIGITS = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}
matcher = re.compile(r"zero|one|two|three|four|five|six|seven|eight|nine")


def parse_line(line: str) -> str:
    parsed_line = ""
    prev = 0

    for match in matcher.finditer(line, overlapped=True):
        parsed_line += line[prev : match.start()] + str(DIGITS[match.group()])
        prev = match.end()

    parsed_line += line[prev:]

    return parsed_line


def find_calibration_value(line: str) -> int:
    i = 0
    j = len(line) - 1

    fd = -1
    ld = -1

    while fd == -1 or ld == -1:
        if fd == -1 and line[i].isdigit():
            fd = line[i]
        if ld == -1 and line[j].isdigit():
            ld = line[j]

        i += 1
        j -= 1

    val = int(f"{fd}{ld}")

    return val


with open("01/input.txt") as cv:
    val_sum_no_parsing = 0
    val_sum_parsing = 0

    for line in cv.readlines():
        parsed_line = parse_line(line)

        val_sum_no_parsing += find_calibration_value(line)
        val_sum_parsing += find_calibration_value(parsed_line)

    print(f"Sum of calibration values (no parsing): {val_sum_no_parsing}")
    print(f"Sum of calibration values (parsing): {val_sum_parsing}")
