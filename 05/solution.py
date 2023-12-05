#!/usr/bin/env python3

import bisect
from dataclasses import dataclass
from functools import total_ordering

# We assume no range in maps overlaps with another range in the same map.
#
# For part 2, the intuition is that, moving through a map, each source interval
# will yield one ore more target intervals, depending on the number of ranges
# falling into that source interval.
# Recursively passing each interval into the next map will eventually lead to a
# sequence of intervals of location positions.
#
#
#                SOURCES                             TARGETS
#                                                                         ======
#                                                                      range A |
#                                                                      targets |
#                                                                              |
#                                                                              |
#                                                                         ======
#
#
# =====                                                                   ======
# | s                                                                          |
# | o                                                                     ======
# | u       =====
# | r       |
# | c       | range A                                                     ======
# | e       | sources                                                  range B |
#           |                                                          targets |
#           =====                                                         ======
# |                                                                       ======
# | i                                                                          |
# | n                                                                     ======
# | t       ======
# | e       | range B
# | r       | sources
# | v       ======
# | a                                                                     ======
# | l                                                                          |
# ======                                                                  ======
#
#
# In the above drawing, the source interval encompasses two ranges (A and B) and
# leads to five target intervals (two for ranges, one before the first range,
# one between range A and B and one after range B).
#
# When we reach the final sequence of location intervals, we can simply look at
# the starting position of the smallest interval in the sequence and compare it
# to the one found for the previous seed interval.
# After having processed all the seed intervals we end up with the smallest
# location position possible.


@dataclass
@total_ordering
class Range:
    source: int
    target: int
    length: int

    def __lt__(self, __value: object) -> bool:
        if isinstance(__value, Range):
            return self.source < __value.source
        else:
            return self.source < __value

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Range):
            return self.source == __value.source
        else:
            return self.source == __value

    @property
    def end(self) -> int:
        return self.source + self.length - 1

    def __repr__(self) -> str:
        return f"[{self.source}, {self.end}]"


class AlmanacMap:
    def __init__(self, name: str) -> None:
        self.name = name
        self.ranges: list[Range] = list()

    def add_range(self, r: Range) -> None:
        bisect.insort(self.ranges, r)

    def __getitem__(self, key: int) -> int:
        range_pos = bisect.bisect_right(self.ranges, key) - 1

        if range_pos < 0 or range_pos >= len(self.ranges):
            return key

        r = self.ranges[range_pos]

        if r.source + r.length - 1 < key:
            return key

        return r.target + (key - r.source)

    def get_target_intervals(
        self, intervals: list[tuple[int, int]]
    ) -> list[tuple[int, int]]:
        target_intervals = list()

        for int_start, int_end in intervals:
            start_range_pos = bisect.bisect_right(self.ranges, int_start) - 1
            stop_range_pos = bisect.bisect_right(self.ranges, int_end)

            if start_range_pos < 0:
                start_range_pos = 0
            if start_range_pos >= len(self.ranges):
                start_range_pos = len(self.ranges) - 1
            if stop_range_pos < 0:
                stop_range_pos = 0
            if stop_range_pos > len(self.ranges):
                stop_range_pos = len(self.ranges)

            # Consider the part of the interval between the start of the
            # interval and the beginning of the first range.
            if int_start < self.ranges[start_range_pos].source:
                target_intervals.append(
                    (int_start, self.ranges[start_range_pos].source)
                )

            for i in range(start_range_pos, stop_range_pos):
                r = self.ranges[i]

                # We need to consider the part which did not overlap located
                # between the end of the previous range and the beginning of the
                # current one
                if i > start_range_pos and r.source > self.ranges[i - 1].end + 1:
                    target_intervals.append((self.ranges[i - 1].end + 1, r.source - 1))

                overlap_start = max(int_start, r.source)
                overlap_end = min(int_end, r.end)

                target_overlap_start = r.target + (overlap_start - r.source)
                target_overlap_end = r.target + (overlap_end - r.source)

                target_intervals.append((target_overlap_start, target_overlap_end))

            # Finally, we need to consider the part of the interval which might
            # be located after the end of the last range, if the end of the
            # interval is greater than the end of the last range
            if int_end > self.ranges[stop_range_pos - 1].end:
                target_intervals.append((self.ranges[stop_range_pos].end + 1, int_end))

        return target_intervals


def parse_map(map_lines: list[str]) -> AlmanacMap:
    name = map_lines[0].rstrip(":")

    almanac_map = AlmanacMap(name)

    for line in map_lines[1:]:
        target, source, length = line.split(" ")
        almanac_map.add_range(Range(int(source), int(target), int(length)))

    return almanac_map


def find_soil(seed: int, maps: list[AlmanacMap]) -> int:
    x = seed

    for almanac_map in maps:
        x = almanac_map[x]

    return x


with open("05/input.txt") as maps_f:
    _, seeds = maps_f.readline().split(":")
    seeds = [int(seed) for seed in seeds.lstrip().split(" ")]

    maps_f.readline()  # Consume the empty line

    map_lines: list[str] = list()
    maps: list[AlmanacMap] = list()

    for line in maps_f.readlines():
        line = line.rstrip("\n")

        if line == "":
            almanac_map = parse_map(map_lines)
            maps.append(almanac_map)

            map_lines.clear()
        else:
            map_lines.append(line)

    almanac_map = parse_map(map_lines)
    maps.append(almanac_map)
    map_lines.clear()

lowest_loc_all_seeds = -1
lowest_loc_ranges = -1

for i in range(0, len(seeds), 2):
    starting_seed = seeds[i]
    seed_range = seeds[i + 1]

    # Solution to part 1
    for seed in [starting_seed, seed_range]:
        soil = find_soil(seed, maps)

        if soil < lowest_loc_all_seeds or lowest_loc_all_seeds == -1:
            lowest_loc_all_seeds = soil

    # Solution to part 2
    x = [(starting_seed, starting_seed + seed_range - 1)]

    for almanac_map in maps:
        x = almanac_map.get_target_intervals(x)

    min_loc = min([interval[0] for interval in x])

    if min_loc < lowest_loc_ranges or lowest_loc_ranges == -1:
        lowest_loc_ranges = min_loc

print(f"Lowest location (list of seeds): {lowest_loc_all_seeds}")
print(f"Lowest location (seed ranges): {lowest_loc_ranges}")
