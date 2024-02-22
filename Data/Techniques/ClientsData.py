from __future__ import annotations
from typing import TYPE_CHECKING
from Data.Techniques.ClientData import ClientData
from Attacks.InitialAccessAttack import InitialAccessAttack
if TYPE_CHECKING:
    from Shells.MetasploitShell import MetasploitC2
    from Data.Techniques.ClientsData import ClientsData
    from Shells.Client import C2Client
    from Attacks.Attack import Attack
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
    
    async def runNextAttack(self, metasploitServer: MetasploitC2, operation: Operation):
        nextAttack, client = self.getNextAttackAndClient(operation)
        # Todo: this seems like a bad way of seperating what clients to run on, fix it
        if(isinstance(nextAttack, InitialAccessAttack)):
            # Todo: fix some bug right here where it just takes forever
            await nextAttack.execute(client, metasploitServer, operation)
            client.attackLog.append(nextAttack)
        else:
            await client.c2Shells[0].executeAttack(nextAttack, operation)
            client.attackLog.append(nextAttack)

    def getNextAttackAndClient(self, operation: Operation):
        for client in self.clients:
            possibleNonUsedAttacks = client.getPossibleNonUsedAttacks(operation.getAttackLibrary());
            try:
                return (self.chooseAttackFromAttacks(possibleNonUsedAttacks), client)
            except Exception as e:
                continue
        return None
    
    def chooseAttackFromAttacks(self, attacks: [Attack]):
        if(len(attacks) == 0):
            raise Exception("No attacks to choose from!")
        return attacks[0]
        
    
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