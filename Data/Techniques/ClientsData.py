from __future__ import annotations
from typing import TYPE_CHECKING
from Data.Techniques.ClientData import ClientData
if TYPE_CHECKING:
    from Data.Techniques.ClientsData import ClientsData
    from Operations.Client import C2Client
    from Attacks.Attack import Attack
    from Attacks.InitialAccessAttack import InitialAccessAttack
    from Operations.Operation import Operation

class ClientsData:
    def __init__(self):
        self.clients: list[ClientData] = []

    def getClientsData(self):
        return self.clients
    
    def getClientData(self, ipAddress: str):
        for client in self.clients:
            if client.ipAddress == ipAddress:
                return client
        return None
    
    # this probably shouldn't only be limited to InitialAccessAttack
    def getClientsWhoMeetPrereqs(self, attack: InitialAccessAttack):
        clientsWhoMeetPreqreqs = []
        for client in self.clients:
            if(attack.meetsPrereqs(client)):
                clientsWhoMeetPreqreqs.append(client)
        return clientsWhoMeetPreqreqs
    
    def getNextAttack(self, operation: Operation):
        for client in self.clients:
            possibleNonUsedAttacks = client.getPossibleNonUsedAttacks(operation.getAttackLibrary());
            if(len(possibleNonUsedAttacks) != 0):
                return possibleNonUsedAttacks[0]
        return None
    
    def runNextAttack(self, operation: Operation):
        for client in self.clients:
            possibleNonUsedAttacks = client.getPossibleNonUsedAttacks(operation.getAttackLibrary());
            if(len(possibleNonUsedAttacks) != 0):
                client.c2Shells[0].executeAttack(possibleNonUsedAttacks[0])
                client.attackLog.append(possibleNonUsedAttacks[0])
        
    
    def getClientsWithServiceFromMetasploitName(self, metasploitName: str):
        clientsWithService: list[C2Client] = []
        for client in self.clients:
            if(client.servicesData.hasServiceNameInMetasploitName(metasploitName)):
                clientsWithService.append(client)
        return clientsWithService

    def addClientData(self, clientData: ClientData):
        self.clients.append(clientData)

    # Assumes first client added is for attacking, and first shell of that client is attacking
    def getAttackC2Client(self):
        attackClient = self.clients[0]
        attackC2 = attackClient.c2Shells[0]
        return attackC2

    def mergeClientData(self, newClientsData: ClientsData):
        for newClientData in newClientsData.getClientsData():
            exists = False
            for client in self.clients:
                if(client.ipAddress == newClientData.ipAddress):
                    exists = True
            
            if(not exists):
                self.clients.append(newClientData)