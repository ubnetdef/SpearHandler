from __future__ import annotations
from typing import TYPE_CHECKING
from Data.Techniques import ServicesData
if TYPE_CHECKING:
    from Attacks.Attack import Attack
    from Operations.Client import C2Client

class ClientData:
    # This design right here of using ipAddresses like a primary key has networking implications I can't think of right now
    def __init__(self, ipAddress, c2Shells=[]):
        self.ipAddress = ipAddress
        self.servicesData: ServicesData.ServicesData = ServicesData.ServicesData()
        self.c2Shells: list[C2Client] = c2Shells
        # Options:
        # linux, windows, freebsd
        operatingSystem = None
        self.attackLog = []
    
    def getPossibleNonUsedAttacks(self, attacks: list[Attack]):
        possibleAttacks = self.getPossibleAttacks(attacks)
        possibleNonUsedAttacks = self.getNonUsedAttacks(possibleAttacks)
        return possibleNonUsedAttacks
    
    def getPossibleAttacks(self, attacks: list[Attack]):
        possibleAttacks = []
        for attack in attacks:
            if(attack.meetsPrereqs(self)): # Why does meetPrereqs use ClientData and not c2client?
                # ^ Cause it uses data of client to check prereqs, makes sense OOP
                possibleAttacks.append(attack)
        return possibleAttacks
    
    def getNonUsedAttacks(self, attacks: [Attack]):
        nonUsedAttacks = []
        for attack in attacks:
            if(attack not in self.attackLog):
                nonUsedAttacks.append(attack)
        return nonUsedAttacks