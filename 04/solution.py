#!/usr/bin/env python3

import re

num_re = re.compile("(\d+)")

with open("04/input.txt") as table_f:
    sum_card_values = 0

    for scratch_card in table_f.readlines():
        splits = scratch_card.split(":")
        card_id = splits[0]
        sequences = splits[1].split("|")

        winning_seq = sequences[0]
        card_seq = sequences[1]

        winning_nos = set([int(number) for number in num_re.findall(winning_seq)])
        card_nos = set([int(number) for number in num_re.findall(card_seq)])

        matches = len(winning_nos.intersection(card_nos))

        card_value = 2 ** (matches - 1) if matches > 0 else 0

        sum_card_values += card_value

    print(f"Sum of card values: {sum_card_values}")
