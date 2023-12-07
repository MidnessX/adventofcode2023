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
CARD_STRENGTHS_ALT = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "J": 1,
}


@total_ordering
class Hand:
    cards: tuple[str, str, str, str, str]
    bid: int
    type: int

    @classmethod
    def _remove_joker(cls, card_counts: list[int, str]) -> int:
        joker_idx = -1

        for i in range(len(card_counts)):
            if card_counts[i][1] == "J":
                joker_idx = i
                break

        if (
            joker_idx >= 0 and len(card_counts) > 1
        ):  # When there are only jokers in the hand we cannot remove them
            joker_val, _ = card_counts.pop(i)
        else:
            joker_val = 0

        card_counts[0] = (card_counts[0][0] + joker_val, card_counts[0][1])

        return card_counts

    @property
    def type(self) -> int:
        card_counts = dict()
        for card in self.cards:
            if card_counts.get(card):
                card_counts[card] += 1
            else:
                card_counts[card] = 1
        card_counts = sorted(
            zip(card_counts.values(), card_counts.keys()), reverse=True
        )

        if self.alt:
            card_counts = self._remove_joker(card_counts)

        if card_counts[0][0] == 5:
            type = HandTypes.FIVE_OF_A_KIND
        elif card_counts[0][0] == 4:
            type = HandTypes.FOUR_OF_A_KIND
        elif card_counts[0][0] == 3 and card_counts[1][0] == 2:
            type = HandTypes.FULL_HOUSE
        elif card_counts[0][0] == 3:
            type = HandTypes.THREE_OF_A_KIND
        elif card_counts[0][0] == 2 and card_counts[1][0] == 2:
            type = HandTypes.TWO_PAIR
        elif card_counts[0][0] == 2:
            type = HandTypes.ONE_PAIR
        else:
            type = HandTypes.HIGH_CARD

        return type

    def __init__(
        self, cards: tuple[str, str, str, str, str], bid: int, alt: bool = False
    ) -> None:
        self.cards = cards
        self.bid = bid
        self.alt = alt

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

        card_strengths = CARD_STRENGTHS_ALT if self.alt else CARD_STRENGTHS

        for card, other_card in zip(self.cards, other.cards):
            if card_strengths[card] > card_strengths[other_card]:
                return True
            if card_strengths[card] < card_strengths[other_card]:
                return False

        return False

    def __repr__(self) -> str:
        return f"cards={str().join(self.cards)}, bid={self.bid}, type={self.type}"


hands: list[Hand] = list()

with open(Path(__file__).parent / "input.txt") as hands_f:
    for hand_l in hands_f:
        cards, bid = hand_l.split(" ")
        hands.append(Hand(tuple(cards), int(bid)))

hands_original = sorted(hands)

for hand in hands:
    hand.alt = True

hands_alt = sorted(hands)

winnings_original = [
    hands_original[rank].bid * (rank + 1) for rank in range(len(hands_original))
]
winnings_alt = [hands_alt[rank].bid * (rank + 1) for rank in range(len(hands_alt))]

print(f"Total winnings (original game): {sum(winnings_original)}")
print(f"Total winnings (alternative game): {sum(winnings_alt)}")
