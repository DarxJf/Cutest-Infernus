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


#BOSS_EVERY_N_BATTLES = 5


class RunState:
    def __init__(self, leaderKey: str, startingSouls: int = 0) -> None:
        self.party = Party(leaderKey=leaderKey)
        self.inventory = Inventory()
        self.wallet = RunWallet(souls=startingSouls)
        self.offers = RestOffers(offerSize=2)

     
        #self.battlesFought = 0
        #self.battlesSinceBoss = 0

        # The offer starts empty; it's rolled the first time you enter
        # the rest area (RestState.enter calls offers.reroll(party)).
        # Nothing to do here yet.



    # def register_battle_won(self) -> bool:
    #     """
    #     Increments the battle counter. Returns True if the next battle
    #     should be a boss fight (once every BOSS_EVERY_N_BATTLES).
    #     """
    #     self.battlesFought += 1
    #     self.battlesSinceBoss += 1

    #     if self.battlesSinceBoss >= BOSS_EVERY_N_BATTLES:
    #         self.battlesSinceBoss = 0
    #         return True
    #     return False

    def is_game_over(self) -> bool:
        """A run ends when every party member is dead."""
        return all(m.dead for m in self.party.members)


    def to_dict(self) -> Dict[str, Any]:
        return {
            "wallet": self.wallet.to_dict(),
            "party": self.party.to_dict(),
            "inventory": self.inventory.to_dict(),
            "battlesFought": self.battlesFought,
            "battlesSinceBoss": self.battlesSinceBoss,
        }

    def load_dict(self, data: Dict[str, Any]) -> None:
        self.wallet.load_dict(data["wallet"])
        self.party.load_dict(data["party"])
        self.inventory.load_dict(data["inventory"])
        self.battlesFought = data.get("battlesFought", 0)
        self.battlesSinceBoss = data.get("battlesSinceBoss", 0)