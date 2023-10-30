from Data.Techniques import ClientData
from typing import List

# Singleton Varible
database = None

class Database():
    clients: List[ClientData.ClientData] = []

    # Singleton
    def __init__():
        global database
        if database != None:
            return database

    def getClientData(self, ipAddress):
        for client in self.clients:
            if client.ipAddress == ipAddress:
                return client