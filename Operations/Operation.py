from Operations.Client import Client
from Attacks.RunNMAP import RunNMAP
from Attacks.Attack import Attack

class Operation():
    inScopeIPs = []
    clients: [Client] = [None]

    def __init__(self, inScopeIPs, clients):
        self.inScopeIPs = inScopeIPs
        self.clients = clients

    def addClient(self, client: Client):
        self.clients.append(client)

    # A operation is intended to start w/ 1 client, that being a kali instance that will be the 'attacker', right off the bat it will then execute nmap
    async def startOperation(self):
        client: Client = self.clients[0]
        await client.executeAttack(RunNMAP("nmaptest"), self)
        # Todo: add more to start of operation here

    async def runAttack(self, client: Client, attack: Attack):
        await client.executeAttack(attack)