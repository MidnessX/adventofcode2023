#!/usr/bin/env python3

from pathlib import Path
from dataclasses import dataclass

SIZE = (10, 10)


@dataclass
class Block:
    id: str
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    z_min: int
    z_max: int
    supports: list["Block"]
    supported_by: list["Block"]

    def __hash__(self) -> int:
        return hash(self.id)


def fall(blocks: list[Block]) -> list[Block]:
    blocks = sorted(blocks, key=lambda b: b.z_min)

    for i, block in enumerate(blocks):
        possible_supports: list[Block] = list()

        # Iterate over blocks below to find out which ones are providing
        # support for the block.
        # It is important to remember that block below may no longer be ordered
        # by ascending Z value, so every one of them must be checked.
        for j in range(i - 1, -1, -1):
            block_below = blocks[j]

            # Check for overlap between the block and that below.
            if (
                block.x_min <= block_below.x_max
                and block.x_max >= block_below.x_min
                and block.y_min <= block_below.y_max
                and block.y_max >= block_below.y_min
            ):
                possible_supports.append(block_below)

        # If possible_supports is empty, it means the block is lying on the
        # ground.
        if len(possible_supports) == 0:
            new_z = 1
        else:
            new_z = max(possible_supports, key=lambda block: block.z_max).z_max

        block.z_max = (
            new_z + 1 + (block.z_max - block.z_min)
        )  # Add one to account for the fact that the block is resting above the support
        block.z_min = new_z + 1

        for support in possible_supports:
            if support.z_max == new_z:
                block.supported_by.append(support)
                support.supports.append(block)

    return blocks


def safe_to_remove(block: Block) -> bool:
    for supported_block in block.supports:
        if len(supported_block.supported_by) <= 1:
            return False

    return True


def count_falling_blocks(block: Block, fallen: set[Block]) -> int:
    # The key here is sharing the set of fallen blocks.
    # If a block (A)is supported by two or more blocks (B and C) which would
    # fall if other blocks below them (D) are removed, the first recursive call
    # for A would return 0 as that block on top still has one or more supports.
    # However, other recursive calls will eventually populate the set with
    # all the supports (B and C), and A will eventually be added to the falling
    # set as it should be.
    #
    #   A
    #  B C
    #   D

    if len(fallen) > 0 and len(set(block.supported_by).difference(fallen)) > 0:
        return 0

    fallen.add(block)

    for s_block in block.supports:
        count_falling_blocks(s_block, fallen)

    # We simply return the cardinality of the set, as after all the recursive
    # calls are completed it represents the entirety of the blocks that would
    # fall.
    return len(fallen)


blocks: list[Block] = list()

with open(Path(__file__).parent / "input.txt") as snap_f:
    for i, line in enumerate(snap_f):
        line = line.rstrip()

        start, end = line.split("~")

        xs, ys, zs = [int(v) for v in start.split(",")]
        xe, ye, ze = [int(v) for v in end.split(",")]

        blocks.append(Block(i, xs, xe, ys, ye, zs, ze, list(), list()))


blocks = fall(blocks)

safe_blocks = list(filter(safe_to_remove, blocks))

print(f"Safely removable blocks: {len(safe_blocks)}.")

fallen_blocks = list(map(lambda block: count_falling_blocks(block, set()) - 1, blocks))

print(f"Sum of falling blocks for each block removed: {sum(fallen_blocks)}.")
