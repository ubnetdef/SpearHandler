from Client import Client

class Operation():
    clients: [Client] = [None]

    def __init__(self, clients):
        self.clients = clients

    def addClient(self, client: Client):
        self.clients.append(client)