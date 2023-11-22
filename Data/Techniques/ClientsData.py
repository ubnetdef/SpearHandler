from __future__ import annotations
from typing import TYPE_CHECKING
from Data.Techniques.ClientData import ClientData
if TYPE_CHECKING:
    from Data.Techniques.ClientsData import ClientsData
    from Operations.Client import Client
    from Attacks.Attack import Attack
    from Attacks.InitialAccessAttack import InitialAccessAttack

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
    
    def getClientsWithServiceFromMetasploitName(self, metasploitName: str):
        clientsWithService: list[Client] = []
        for client in self.clients:
            if(client.servicesData.hasServiceNameInMetasploitName(metasploitName)):
                clientsWithService.append(client)
        return clientsWithService

    def addClientData(self, clientData: ClientData):
        self.clients.append(clientData)

    def mergeClientData(self, newClientsData: ClientsData):
        for newClientData in newClientsData.getClientsData():
            exists = False
            for client in self.clients:
                if(client.ipAddress == newClientData.ipAddress):
                    exists = True
            
            if(not exists):
                self.clients.append(newClientData)