#!/usr/bin/env python3

from pathlib import Path


def hash_algo(seq: str) -> int:
    val = 0

    for c in seq:
        val += ord(c)
        val *= 17
        val = val % 256

    return val


hash_sum = 0

with open(Path(__file__).parent / "input.txt") as init_f:
    for line in init_f.readlines():
        for step in line.rstrip().split(","):
            hash_sum += hash_algo(step)

print(f"HASH sum: {hash_sum}")
