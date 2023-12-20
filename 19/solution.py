#!/usr/bin/env python3

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Rule:
    dest: str
    target: str = None
    op: str = None
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
            op = lhs[1]
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

            if (
                part[rule.target] > rule.value
                if rule.op == ">"
                else part[rule.target] < rule.value
            ):
                dest = rule.dest
                break

        if dest == "R":
            return 0
        if dest == "A":
            return sum(part.values())

        wf_name = dest


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
    f"Sum of ratings of accepted parts: {sum(map(lambda pt: sum_ratings(workflows, pt), parts))}"
)
