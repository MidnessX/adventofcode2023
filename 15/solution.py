#!/usr/bin/env python3

from pathlib import Path
import re

step_re = re.compile(r"(\w+)(-|=)(\d*)")

# Why use a hash table to implement a hash table? :P


def hash_algo(seq: str) -> int:
    val = 0

    for c in seq:
        val += ord(c)
        val *= 17
        val = val % 256

    return val


def focusing_power(boxes: list[list[tuple[str, int]]]) -> int:
    power = 0

    for box_id, box in enumerate(boxes):
        for slot, (_, lens_fl) in enumerate(box):
            power += (box_id + 1) * (slot + 1) * lens_fl

    return power


hash_sum = 0
boxes = [list() for _ in range(256)]

with open(Path(__file__).parent / "input.txt") as init_f:
    for line in init_f.readlines():
        for step in line.rstrip().split(","):
            hash_sum += hash_algo(step)

            label, op, val = step_re.match(step).groups()

            box = hash_algo(label)

            found = False

            for i, (lens_lbl, lens_fl) in enumerate(boxes[box]):
                if lens_lbl == label:
                    if op == "-":
                        del boxes[box][i]
                    if op == "=":
                        boxes[box][i] = (label, int(val))
                    found = True
                    break

            if op == "=" and not found:
                boxes[box].append((label, int(val)))

print(f"HASH sum: {hash_sum}")
print(f"HASHMAP focusing power: {focusing_power(boxes)}")
