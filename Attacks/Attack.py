from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Operations.Client import Client
    from Operations.Operation import Operation

class Attack:
    def __init__(self, AttackName):
        self.name = AttackName

    def execute(self, client: Client, operation: Operation):
        # Todo: Really should actually throw error here
        pass