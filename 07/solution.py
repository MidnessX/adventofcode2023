#!/usr/bin/env python3

from functools import total_ordering
from typing import Any
from enum import IntEnum, auto
from pathlib import Path


class HandTypes(IntEnum):
    HIGH_CARD = auto()
    ONE_PAIR = auto()
    TWO_PAIR = auto()
    THREE_OF_A_KIND = auto()
    FULL_HOUSE = auto()
    FOUR_OF_A_KIND = auto()
    FIVE_OF_A_KIND = auto()


CARD_STRENGTHS = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}


@total_ordering
class Hand:
    cards: tuple[str, str, str, str, str]
    bid: int
    type: int

    def __init__(self, cards: tuple[str, str, str, str, str], bid: int) -> None:
        self.cards = cards
        self.bid = bid

        card_counts = dict()
        for card in self.cards:
            if card_counts.get(card):
                card_counts[card] += 1
            else:
                card_counts[card] = 1
        card_counts = sorted(
            zip(card_counts.values(), card_counts.keys()), reverse=True
        )

        if card_counts[0][0] == 5:
            self.type = HandTypes.FIVE_OF_A_KIND
        elif card_counts[0][0] == 4:
            self.type = HandTypes.FOUR_OF_A_KIND
        elif card_counts[0][0] == 3 and card_counts[1][0] == 2:
            self.type = HandTypes.FULL_HOUSE
        elif card_counts[0][0] == 3:
            self.type = HandTypes.THREE_OF_A_KIND
        elif card_counts[0][0] == 2 and card_counts[1][0] == 2:
            self.type = HandTypes.TWO_PAIR
        elif card_counts[0][0] == 2:
            self.type = HandTypes.ONE_PAIR
        else:
            self.type = HandTypes.HIGH_CARD

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Hand):
            return False

        return self.cards == other.cards

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, Hand):
            raise NotImplementedError()

        if self.type > other.type:
            return True
        if self.type < other.type:
            return False

        for card, other_card in zip(self.cards, other.cards):
            if CARD_STRENGTHS[card] > CARD_STRENGTHS[other_card]:
                return True
            if CARD_STRENGTHS[card] < CARD_STRENGTHS[other_card]:
                return False

        return False

    def __repr__(self) -> str:
        return f"cards={str().join(self.cards)}, bid={self.bid}, type={self.type}"


hands: list[Hand] = list()

with open(Path(__file__).parent / "input.txt") as hands_f:
    for hand_l in hands_f:
        cards, bid = hand_l.split(" ")
        hands.append(Hand(tuple(cards), int(bid)))

hands = sorted(hands)

winnings = [hands[rank].bid * (rank + 1) for rank in range(len(hands))]

print(f"Total winnings: {sum(winnings)}")
