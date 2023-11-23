from Operations.Client import Client
from Attacks.RunNMAP import RunNMAP
from Attacks.Attack import Attack
from Data.Techniques.ClientsData import ClientsData
from Data.Techniques.ClientData import *
from Attacks.ServiceStopper import ServiceStoppe

class Operation():
    def __init__(self, inScopeIPs=[], clients=ClientsData()):
        self.inScopeIPs = inScopeIPs
        self.clientsData: ClientsData = clients
        self.attackLibrary: list[Attack] = []

    def addAttack(self, attack: Attack):
        self.attackLibrary.append(attack)

    def registerAllInScope(self):
        clientsData = ClientsData()
        for inScopeIP in self.inScopeIPs:
            clientData = ClientData(inScopeIP)
            clientsData.addClientData(clientData)
        return clientsData

    async def scanAll(self, attackClient: Client):
        for clientData in self.clientsData.clients:
            ip = clientData.ipAddress
            # Working here
            await attackClient.executeAttack(RunNMAP("nmaptest"), self)

    
    # A operation is intended to start w/ 1 client, that being a kali instance that will be the 'attacker', right off the bat it will then execute nmap
    async def startOperation(self):
        client: Client = self.c2Clients[0]
        await self.scanAll()
        
        # await client.executeAttack(RunNMAP("nmaptest"), self)
        # # Todo: add more to start of operation here
        # testUbuntu: Client = self.c2Clients[1]
        # await testUbuntu.executeAttack(ServiceStopper("servicestopped"), self)

    async def runAttack(self, clientData: ClientData, attack: Attack):
        await clientData.c2Shell.executeAttack(attack)