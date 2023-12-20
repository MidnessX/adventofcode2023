#!/usr/bin/env python3

from dataclasses import dataclass
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


@dataclass
class RxModule(Module):
    machine_active: bool = False

    def pulse(self, module: str, pulse: bool) -> list[tuple[str, bool]]:
        if not pulse:
            self.machine_active = True

        return list()


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

    rx_module = None

    # Add inputs to ConjunctionModule instances
    for module_name, module in modules.items():
        for conn_name in module.conns:
            conn = modules.get(conn_name)

            if conn is None:
                # We must handle end modules which have no entry in the file.
                # We instantiate one on the fly.
                conn = RxModule(conn_name, list())
                rx_module = conn

            if isinstance(conn, ConjunctionModule):
                conn.inputs[module_name] = False

    if rx_module is not None:
        modules[rx_module.name] = rx_module

    return modules


def push(modules: dict[str, Module]) -> tuple[int, int]:
    pulses = [("button", "broadcaster", False)]
    low_p = 0
    high_p = 0

    while True:
        try:
            sender_name, dest_name, val = pulses.pop(0)
        except IndexError:
            break

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


modules = load_modules()
rx_module = modules["rx"]

i = 0
while not rx_module.machine_active:
    i += 1
    push(modules)

print(f"Minimum number of pushes to activate RX module: {i}.")
