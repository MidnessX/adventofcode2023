#!/usr/bin/env python3

from pathlib import Path


def predict(sequence: list[int], start: bool = False) -> int:
    history = [sequence[0]] if start else [sequence[-1]]

    while any(sequence):
        sequence = [sequence[j + 1] - sequence[j] for j in range(len(sequence) - 1)]

        history.append(sequence[0] if start else sequence[-1])

    if start:
        pred = 0
        for i in range(len(history) - 1, -1, -1):
            pred = history[i] - pred

        return pred

    return sum(history)


with open(Path(__file__).parent / "input.txt") as seq_f:
    sequences = [[int(x) for x in line.split(" ")] for line in seq_f.readlines()]

# Part 1
end_predictions = map(predict, sequences)
# Part 2
start_predictions = map(lambda sequence: predict(sequence, start=True), sequences)

print(f"Sum of end predictions: {sum(end_predictions)}")
print(f"Sum of start predictions: {sum(start_predictions)}")
