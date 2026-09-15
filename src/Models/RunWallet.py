"""
Mutable wallet. Wrapping the soul count in an object lets it travel by
reference through the state stack: any state that receives the wallet
can spend or gain souls, and the change is visible to everyone else.
"""

from typing import Any, Dict


class RunWallet:
    def __init__(self, souls: int = 0) -> None:
        self.souls = souls

    def can_afford(self, amount: int) -> bool:
        return self.souls >= amount

    def spend(self, amount: int) -> bool:
        if not self.can_afford(amount):
            return False
        self.souls -= amount
        return True

    def earn(self, amount: int) -> None:
        self.souls += amount


    def to_dict(self) -> Dict[str, Any]:
        return {"souls": self.souls}

    def load_dict(self, data: Dict[str, Any]) -> None:
        self.souls = data.get("souls", 0)