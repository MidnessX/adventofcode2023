#!/usr/bin/env python3

import re
from dataclasses import dataclass

game_re = re.compile(r"Game (\d+)")
observation_re = re.compile(r"(\d+) (red|green|blue)")


@dataclass
class Observation:
    red: int = 0
    green: int = 0
    blue: int = 0

    def __str__(self) -> str:
        return f"R: {self.red}\tG: {self.green}\tB: {self.blue}"


def parse_observation(game_observation: str) -> Observation:
    observation = Observation()

    for cube in observation_re.finditer(game_observation):
        num = int(cube.groups()[0])
        color = cube.groups()[1]

        setattr(observation, color, num)

    if observation.red == 0 and observation.green == 0 and observation.blue == 0:
        raise ValueError()

    return observation


def parse_line(line: str) -> tuple[int, list[Observation]]:
    parts = line.split(":")

    game_info = parts[0]
    game_observations = parts[1]

    game_id = int(game_re.match(game_info).groups()[0])
    observations = [
        parse_observation(game_observation)
        for game_observation in game_observations.split(";")
    ]

    return game_id, observations


with open("02/input.txt", "r") as games_f:
    game_id_sum = 0

    for line in games_f.readlines():
        game_id, observations = parse_line(line)

        valid = True

        for observation in observations:
            if observation.red > 12 or observation.green > 13 or observation.blue > 14:
                valid = False
                break

        if valid:
            game_id_sum += game_id

print(f"Sum of valid game IDs: {game_id_sum}")
