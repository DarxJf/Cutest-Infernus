"""
Manages the current rest-area offer: which secondary characters are
visible this visit. Rerolls on demand from the pool of secondaries,
excluding those already in the party.
"""

import random
from typing import List

from src.Definitions.Entity import get_secondary_characters
from src.Models.Party import Party


DEFAULT_OFFER_SIZE = 3


class RestOffers:
    def __init__(self, offerSize: int = DEFAULT_OFFER_SIZE) -> None:
        self.offerSize = offerSize
        self.currentKeys: List[str] = []

    def reroll(self, party: Party) -> None:
        pool = [
            k for k in get_secondary_characters().keys()
            if not party.has(k)
        ]

        random.shuffle(pool)
        self.currentKeys = pool[: self.offerSize]

    def all(self) -> List[str]:
        return list(self.currentKeys)

    def remove(self, key: str) -> None:
        if key in self.currentKeys:
            self.currentKeys.remove(key)

    def isEmpty(self) -> bool:
        return len(self.currentKeys) == 0