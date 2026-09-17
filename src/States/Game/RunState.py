"""
RunState: everything that lives for the duration of a single run
(party, inventory, wallet, offers, boss counter). Created when the
player picks a main character, destroyed on game over.

This is the object that the rest area, battles and save/load all pass
by reference, so mutations are visible everywhere without copying.
"""

from typing import Any, Dict

from src.Models.Party import Party
from src.Models.Inventory import Inventory
from src.Models.RestOffers import RestOffers
from src.Models.RunWallet import RunWallet


BOSS_EVERY_N_BATTLES = 5


class RunState:
    def __init__(self, leaderKey: str, startingSouls: int = 0) -> None:
        self.party = Party(leaderKey=leaderKey)
        self.inventory = Inventory()
        self.wallet = RunWallet(souls=startingSouls)
        self.offers = RestOffers(offerSize=2)

     
        self.battlesFought = 0
        self.battlesSinceBoss = 0

        self.seenIntro = False
        self.seenPlayTutorial = False
        self.seenRestTutorial = False
        self.seenBattleTutorial = False


    def register_battle_won(self) -> bool:
        """
        Increments the battle counter. Returns True if the next battle
        should be a boss fight (once every BOSS_EVERY_N_BATTLES).
        """
        self.battlesFought += 1
        self.battlesSinceBoss += 1

        if self.battlesSinceBoss >= BOSS_EVERY_N_BATTLES:
            self.battlesSinceBoss = 0
            return True
        return False

    def shouldSpawnBoss(self) -> bool:
        return self.battlesSinceBoss + 1 >= BOSS_EVERY_N_BATTLES

    def is_game_over(self) -> bool:
        leader = self.party.lead()
        return leader is None or leader.dead
    

    def to_dict(self) -> Dict[str, Any]:
        return {
            "wallet": self.wallet.to_dict(),
            "party": self.party.to_dict(),
            "inventory": self.inventory.to_dict(),
            "battlesFought": self.battlesFought,
            "battlesSinceBoss": self.battlesSinceBoss,
            "seenIntro": self.seenIntro,
            "seenPlayTutorial": self.seenPlayTutorial,
            "seenRestTutorial": self.seenRestTutorial,
            "seenBattleTutorial": self.seenBattleTutorial,
        }

    def load_dict(self, data: Dict[str, Any]) -> None:
        self.wallet.load_dict(data["wallet"])
        self.party.load_dict(data["party"])
        self.inventory.load_dict(data["inventory"])
        self.battlesFought = data.get("battlesFought", 0)
        self.battlesSinceBoss = data.get("battlesSinceBoss", 0)
        self.seenIntro = data.get("seenIntro", False)
        self.seenPlayTutorial = data.get("seenPlayTutorial", False)
        self.seenRestTutorial = data.get("seenRestTutorial", False)
        self.seenBattleTutorial = data.get("seenBattleTutorial", False)