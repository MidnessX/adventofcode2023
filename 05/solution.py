#!/usr/bin/env python3

import bisect
from dataclasses import dataclass
from functools import total_ordering

# We assume no range in maps overlaps with another range in the same map.


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


def parse_map(map_lines: list[str]) -> AlmanacMap:
    name = map_lines[0].rstrip(":")

    almanac_map = AlmanacMap(name)

    for line in map_lines[1:]:
        target, source, length = line.split(" ")
        almanac_map.add_range(Range(int(source), int(target), int(length)))

    return almanac_map


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

lowest_loc = -1

for seed in seeds:
    x = seed

    for almanac_map in maps:
        x = almanac_map[x]

    if x < lowest_loc or lowest_loc == -1:
        lowest_loc = x

print(f"Lowest location: {lowest_loc}")
