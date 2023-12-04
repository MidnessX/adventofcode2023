#!/usr/bin/env python3

import re

num_re = re.compile("(\d+)")

with open("04/input.txt") as table_f:
    sum_card_values = 0

    card_copies = list()

    for scratch_card in table_f.readlines():
        splits = scratch_card.split(":")

        card_id = int(num_re.search(splits[0]).group())

        if card_id == 71:
            pass

        if len(card_copies) >= card_id:
            card_copies[card_id - 1] += 1
        else:
            card_copies.append(1)  # We have at least one copy of each scratchcard

        sequences = splits[1].split("|")

        winning_seq = sequences[0]
        card_seq = sequences[1]

        winning_nos = set([int(number) for number in num_re.findall(winning_seq)])
        card_nos = set([int(number) for number in num_re.findall(card_seq)])

        matches = len(winning_nos.intersection(card_nos))

        if matches > 0:
            for i in range(card_id, card_id + matches):
                if len(card_copies) > i:
                    card_copies[i] += card_copies[card_id - 1]
                else:
                    card_copies.append(card_copies[card_id - 1])

        card_value = 2 ** (matches - 1) if matches > 0 else 0

        sum_card_values += card_value

    print(f"Sum of card values: {sum_card_values}")
    print(f"Total number of scratchcards: {sum(card_copies)}")
