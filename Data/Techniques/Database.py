from Data.Techniques.ClientData import ClientData
from typing import List

# Todo: Review this, maybe should be singleton, idk

class Database():
    clients: List[ClientData] = []

    def addClientData(self, ipAddress):
        clientData = ClientData(ipAddress)
        self.clients.append(clientData)
        return ClientData(ipAddress)

    def getClientData(self, ipAddress):
        for client in self.clients:
            if client.ipAddress == ipAddress:
                return client
        return None

    def getOrAddClientData(self, ipAddress):
        clientData = self.getClientData(ipAddress)

        if(clientData == None):
            clientData = self.addClientData(ipAddress)
        return clientData

