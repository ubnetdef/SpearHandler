from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Operations.Client import C2Client
    from Operations.Operation import Operation
    from Data.Techniques.ClientData import ClientData

class Attack:
    def __init__(self, AttackName):
        self.name = AttackName

    def execute(self, client: C2Client, operation: Operation):
        # Todo: Really should actually throw error here
        pass

    def meetsPrereqs(self, clientData: ClientData):
        # Todo: Really should actually throw error here
        pass