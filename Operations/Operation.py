from Operations.Client import Client
from Attacks.RunNMAP import RunNMAP
from Attacks.Attack import Attack
from Data.Techniques.ClientsData import ClientsData
from Data.Techniques.ClientData import *
from Attacks.ServiceStopper import ServiceStopper

class Operation():
    def __init__(self, inScopeIPs=[], clients=ClientsData()):
        self.inScopeIPs = inScopeIPs
        self.clientsData: ClientsData = clients
        self.c2Clients: list[Client] = []

    def addC2Client(self, client: Client):
        self.c2Clients.append(client)

    # A operation is intended to start w/ 1 client, that being a kali instance that will be the 'attacker', right off the bat it will then execute nmap
    async def startOperation(self):
        client: Client = self.c2Clients[0]
        await client.executeAttack(RunNMAP("nmaptest"), self)
        # Todo: add more to start of operation here
        testUbuntu: Client = self.c2Clients[1]
        await testUbuntu.executeAttack(ServiceStopper("servicestopped"), self)

    async def runAttack(self, clientData: ClientData, attack: Attack):
        await clientData.c2Client.executeAttack(attack)