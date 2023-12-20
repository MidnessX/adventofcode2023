#!/usr/bin/env python3

from copy import deepcopy
from dataclasses import dataclass
from functools import reduce
from pathlib import Path
from typing import Callable

operations = {">": lambda x, y: x > y, "<": lambda x, y: x < y}


@dataclass
class Rule:
    dest: str
    target: str = None
    op: Callable = None
    value: int = None


def decode_workflow(line: str) -> tuple[str, list[Rule]]:
    rule_list = list()

    name, rules = line.split("{")

    rules = rules[:-1]  # Discard trailing }
    rules = rules.split(",")

    for i, rule in enumerate(rules):
        if i < len(rules) - 1:
            lhs, dest = rule.split(":")
            target = lhs[0]
            op = operations[lhs[1]]
            value = int(lhs[2:])

            rule_list.append(Rule(dest, target=target, op=op, value=value))
        else:
            rule_list.append(Rule(rule))

    return name, rule_list


def decode_part(line: str) -> dict[str, int]:
    part = dict()

    line = line[1:-1]  # Remove { and }
    attrs = line.split(",")

    for attr in attrs:
        key = attr[0]
        value = int(attr[2:])

        part[key] = value

    return part


def sum_ratings(workflows: dict[str, list[Rule]], part: dict[str, int]) -> int:
    wf_name = "in"

    while True:
        wf = workflows[wf_name]

        for rule in wf:
            if rule.target is None:
                dest = rule.dest
                break

            if rule.op(part[rule.target], rule.value):
                dest = rule.dest
                break

        if dest == "R":
            return 0
        if dest == "A":
            return sum(part.values())

        wf_name = dest


def get_combinations(boundaries: dict[str, int]) -> int:
    intervals = [h - l + 1 for l, h in boundaries.values()]

    return reduce(lambda x, y: x * y, intervals)


def workflow_combinations(
    workflow_name: str, workflows: dict[str, list[Rule]], boundaries: dict[str, int]
) -> int:
    workflow = workflows[workflow_name]
    combinations = 0

    for rule in workflow:
        if rule.target is None:
            if rule.dest == "A":
                return combinations + get_combinations(boundaries)
            elif rule.dest == "R":
                return combinations
            else:
                return combinations + workflow_combinations(
                    rule.dest, workflows, boundaries
                )

        # other_bd represents boundaries which trigger the current rule and is
        # used when we recursively calculate possible combinations for that
        # rule.
        other_bd = deepcopy(boundaries)

        if rule.op == operations["<"]:
            other_bd[rule.target][1] = rule.value - 1
            boundaries[rule.target][0] = rule.value
        else:
            other_bd[rule.target][0] = rule.value + 1
            boundaries[rule.target][1] = rule.value

        if rule.dest == "A":
            combinations += get_combinations(other_bd)
        elif rule.dest == "R":
            continue
        else:
            combinations += workflow_combinations(rule.dest, workflows, other_bd)


with open(Path(__file__).parent / "input.txt") as parts_f:
    workflows = dict()
    parts = list()

    split = False

    for line in parts_f.readlines():
        line = line.rstrip()

        if line == "":
            split = True
            continue

        if split:
            parts.append(decode_part(line))
        else:
            name, rules = decode_workflow(line)
            workflows[name] = rules

print(
    f"Sum of ratings of accepted parts: {sum(map(lambda pt: sum_ratings(workflows, pt), parts))}."
)

combs = workflow_combinations(
    "in",
    workflows,
    {
        "x": [1, 4000],
        "m": [1, 4000],
        "a": [1, 4000],
        "s": [1, 4000],
    },
)

print(f"Possible combinations: {combs}.")
