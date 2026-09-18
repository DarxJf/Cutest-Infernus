"""
Manages the current shop offer: which passive objects are visible
this visit. Rerolls on demand from the full pool of PASSIVE_OBJECTS.
"""

import random
from typing import List

from src.Definitions.Objects import PASSIVE_OBJECTS


DEFAULT_OFFER_SIZE = 4


class ShopOffers:
    def __init__(self, offerSize: int = DEFAULT_OFFER_SIZE) -> None:
        self.offerSize = offerSize
        self.currentKeys: List[str] = []

    def reroll(self) -> None:
       
        pool = list(PASSIVE_OBJECTS.keys())
        random.shuffle(pool)
        self.currentKeys = pool[: self.offerSize]

    def all(self) -> List[str]:
        return list(self.currentKeys)

    def remove(self, key: str) -> None:
        if key in self.currentKeys:
            self.currentKeys.remove(key)

    def isEmpty(self) -> bool:
        return len(self.currentKeys) == 0