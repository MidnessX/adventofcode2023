#!/usr/bin/env python3

import re
from dataclasses import dataclass


@dataclass
class Race:
    time: int
    distance: int


def search(start: int, end: int, comp_f: callable) -> int | None:
    if start == end:
        return start

    middle = (start + end) // 2  # Check

    if comp_f(middle):
        x = search(start, middle, comp_f)
        return x
    else:
        x = search(middle + 1, end, comp_f)
        return x


def get_ranges(race: Race) -> tuple[int, int]:
    min_press = search(
        0, race.time, lambda hold_t: (race.time - hold_t) * hold_t > race.distance
    )
    max_press = search(
        0, race.time, lambda hold_t: (race.time - hold_t) * hold_t <= race.distance
    )

    return (min_press, max_press)


num_re = re.compile(r"(\d+)")

with open("06/input.txt") as race_f:
    times = race_f.readline().split(":")[1]
    distances = race_f.readline().split(":")[1]

times = [int(val.group()) for val in num_re.finditer(times)]
distances = [int(val.group()) for val in num_re.finditer(distances)]

# For part two.
single_time = int(str().join([str(val) for val in times]))
single_distance = int(str().join([str(val) for val in distances]))

records = [Race(time, distance) for time, distance in zip(times, distances)]

multiple_races_possibilities = 1
for race in records:
    min_press, max_press = get_ranges(race)
    multiple_races_possibilities *= max_press - min_press

# Part two.
min_press, max_press = get_ranges(Race(single_time, single_distance))
single_race_possibilities = max_press - min_press

print(f"Total number of possibilities (muliple races): {multiple_races_possibilities}")
print(f"Total number of possibilities (single race): {single_race_possibilities}")
