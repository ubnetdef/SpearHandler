from Operations.Client import C2Client
from Attacks.RunNMAP import RunNMAP
from Attacks.Attack import Attack
from Data.Techniques.ClientsData import ClientsData
from Data.Techniques.ClientData import *
from Attacks.ServiceStopper import ServiceStopper
from Operations.MetasploitShell import MetasploitC2

class Operation():
    def __init__(self, inScopeIPs=[], clients=ClientsData()):
        self.inScopeIPs = inScopeIPs
        self.clientsData: ClientsData = clients
        self.attackLibrary: list[Attack] = []
    
    # A operation is intended to start w/ 1 client, that being a kali instance that will be the 'attacker', right off the bat it will then execute nmap
    async def startOperation(self, metasploitServer: MetasploitC2):
        attackClient: C2Client = self.clientsData.getAttackC2Client()
        await self.scanAll(attackClient)
        await self.startInitialAccess(metasploitServer)
        await self.stopRandomServiceOnAllClients()
        
        # await client.executeAttack(RunNMAP("nmaptest"), self)
        # # Todo: add more to start of operation here
        # testUbuntu: Client = self.c2Clients[1]
        # await testUbuntu.executeAttack(ServiceStopper("servicestopped"), self)

    async def scanAll(self, attackClient: C2Client):
        await attackClient.executeAttack(RunNMAP("nmaptest"), self)

    async def startInitialAccess(self, metasploitServer: MetasploitC2):
        nextAttack, _ = self.clientsData.getNextAttackAndClient(self)
        while(nextAttack != None):
            try:
                await self.clientsData.runNextAttack(metasploitServer, self)
                nextAttack = self.clientsData.getNextAttackAndClient(self)
            except Exception as e:
                continue
        self.clientsData.clients.pop(0)

    async def stopRandomServiceOnAllClients(self):
        for client in self.clientsData.clients:
            try:
                shell: C2Client = client.c2Shells[0]
                await shell.executeAttack(ServiceStopper("service stopper"), self)
            except Exception as e:
                pass

    async def runAttack(self, clientData: ClientData, attack: Attack):
        await clientData.c2Shell.executeAttack(attack)

    def addAttack(self, attack: Attack):
        self.attackLibrary.append(attack)

    def registerAllInScope(self):
        clientsData = ClientsData()
        for inScopeIP in self.inScopeIPs:
            clientData = ClientData(inScopeIP)
            clientsData.addClientData(clientData)
        return clientsData
    
    def getAttackLibrary(self):
        return self.attackLibrary