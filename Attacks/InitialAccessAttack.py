from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Data.Techniques.ClientData import ClientData
    from Operations.Operation import Operation
    from Operations.MetasploitShell import *

class InitialAccessAttack:
    def __init__(self, AttackName):
        self.name = AttackName

    def meetsPrereqs():
        # Todo: Really should actually throw error here
        pass

    def execute(self, targedHost: ClientData, metasploitServer: MetasploitC2, operation: Operation):
        # Todo: Really should actually throw error here
        pass