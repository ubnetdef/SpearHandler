from __future__ import annotations
from Attacks import Attack
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Operations.Operation import Operation
    from Data.Techniques.ClientData import ClientData

class C2Client():
    def __init__():
        id = None
        ipAddress = None

    async def executeAttack(self, attack: Attack.Attack, operation: Operation):
        await attack.execute(self, operation)

    def executeShell(string):
        raise NotImplementedError("executeShell in client not implemented!")
    
class Client():
    def __init__(self, clientData: ClientData, c2Clients: list[C2Client]):
        self.clientData = clientData
        self.c2Clients = c2Clients