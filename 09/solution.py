#!/usr/bin/env python3

from pathlib import Path


def predict(sequence: list[int]) -> int:
    i = 0
    history = [sequence[-1]]

    while any(sequence):
        sequence = [sequence[j + 1] - sequence[j] for j in range(len(sequence) - 1)]
        history.append(sequence[-1])

        i += 1

    return sum(history)


with open(Path(__file__).parent / "input.txt") as seq_f:
    sequences = [[int(x) for x in line.split(" ")] for line in seq_f.readlines()]

predictions = map(predict, sequences)

print(f"Sum of predictions: {sum(predictions)}")
