#!/usr/bin/env python3

from dataclasses import dataclass
from math import lcm
from pathlib import Path


@dataclass
class Module:
    name: str
    conns: list[str]

    def pulse(self, module: str, pulse: bool) -> list[tuple[str, bool]]:
        return list()


@dataclass
class FlipFlopModule(Module):
    state: bool = False

    def pulse(self, module: str, pulse: bool) -> list[tuple[str, bool]]:
        if not pulse:
            self.state = not self.state

            return [(self.name, conn, self.state) for conn in self.conns]

        return list()


@dataclass
class ConjunctionModule(Module):
    inputs: dict[str, bool]

    def pulse(self, module: str, pulse: bool) -> list[tuple[str, bool]]:
        self.inputs[module] = pulse

        if all(self.inputs.values()):
            return [(self.name, conn, False) for conn in self.conns]

        return [(self.name, conn, True) for conn in self.conns]


@dataclass
class BroadcastModule(Module):
    def pulse(self, module: str, pulse: bool) -> list[tuple[str, bool]]:
        return [(self.name, conn, pulse) for conn in self.conns]


def load_modules() -> dict[str, Module]:
    modules: dict[str, Module] = dict()

    with open(Path(__file__).parent / "input.txt") as config_f:
        for line in config_f.readlines():
            line = line.rstrip()

            name, conns = line.split("->")
            name = name.rstrip()
            conns = conns.lstrip()

            conns = [conn.lstrip() for conn in conns.split(",")]

            if name[0] == "%":
                module = FlipFlopModule(name=name[1:], conns=conns)
            elif name[0] == "&":
                module = ConjunctionModule(name=name[1:], conns=conns, inputs=dict())
            else:
                module = BroadcastModule(name=name, conns=conns)

            name = name[1:] if not isinstance(module, BroadcastModule) else name

            modules[name] = module

    # Add inputs to ConjunctionModule instances
    for module_name, module in modules.items():
        for conn_name in module.conns:
            conn = modules.get(conn_name)

            if conn is None:
                continue

            if isinstance(conn, ConjunctionModule):
                conn.inputs[module_name] = False

    return modules


def push(modules: dict[str, Module], watch: tuple[str, bool] = None) -> tuple[int, int]:
    pulses = [("button", "broadcaster", False)]
    low_p = 0
    high_p = 0

    while True:
        try:
            sender_name, dest_name, val = pulses.pop(0)
        except IndexError:
            break

        if watch and dest_name == watch[0] and val == watch[1]:
            return (None, None)

        low_p += 1 if not val else 0
        high_p += 1 if val else 0

        dest = modules.get(dest_name, None)

        if dest is None:
            continue

        res_pulses = dest.pulse(sender_name, val)
        pulses.extend(res_pulses)

    return (low_p, high_p)


def total_pulses(modules: dict[str, Module]) -> tuple[int, int]:
    i = 0
    cycle = -1
    lpc = 0
    hpc = 0
    fp = list(filter(lambda x: isinstance(x, FlipFlopModule), modules.values()))
    prev_states = [[(module.name, module.state) for module in fp]]

    while i < 1000:
        i += 1

        low_p, high_p = push(modules)
        lpc += low_p
        hpc += high_p

        state = [(module.name, module.state) for module in fp]

        if cycle == -1 and state in prev_states:
            cycle = i

            skips = (1000 - cycle) // cycle

            i += skips * cycle
            lpc += skips * lpc
            hpc += skips * hpc
        else:
            prev_states.append(state)

    return lpc, hpc


modules = load_modules()
lpc, hpc = total_pulses(modules)

print(f"Multiplication of total pulses sent after 1000 cycles: {lpc * hpc}.")


# Part 2 is ugly, but I'm too tired to improve it. Not even sure how much
# better it can become.
# Basically, we get modules connected to the module connected to RX.
# We assume both the module connected to RX and its ancestors to be of the
# ConjunctionModule kind, or this won't work.
# Ancestors must all output a high signal simultaneously in order for the
# module connected to RX to output a low signal, triggering the start of the
# machine connected to RX.
# With this information it's trivial to recognize we have to find the occurrence
# of a low signal being delivered to one of the ancestors in order to determine
# its activation cycle length.
# Once we do this for all the ancestors, using the LCM we can determine the
# minimum number of steps required for RX to receive a low pulse.

cycles = {name: 0 for name in ["gt", "vr", "nl", "lr"]}

for module_name in cycles.keys():
    modules = load_modules()

    i = 0
    retval = (-1, -1)

    while retval != (None, None):
        retval = push(modules, watch=(module_name, False))
        i += 1

    cycles[module_name] = i


print(f"Minimum number of pushes to activate RX module: {lcm(*cycles.values())}.")
