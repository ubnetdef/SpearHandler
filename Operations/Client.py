from __future__ import annotations
from Attacks import Attack
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Operations.Operation import Operation

class Client():

    def __init__():
        id = None
        ipAddress = None

    async def executeAttack(self, attack: Attack.Attack, operation: Operation):
        await attack.execute(self, operation)

    def executeShell(string):
        raise NotImplementedError("executeShell in client not implemented!")