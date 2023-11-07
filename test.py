from Operations import Operation, MythicClient
from Operations.MythicClient import MythicC2, MythicClient
from mythic.mythic_classes import Mythic
import asyncio

async def main():
    inScopeIPs = ["192.168.13.28"]
    clients = []

    testOperation = Operation.Operation(inScopeIPs, clients)

    displayID = 123
    startKaliClient = MythicClient.MythicClient(displayID)
    await startKaliClient.initializeMythic()

    testOperation.addClient(startKaliClient)

    #await testOperation.startOperation()
    await testOperation.runAttack()

async def main2():
    mythic: MythicC2 = await MythicC2().connect()
    clients: list[MythicClient] = await mythic.getActiveClients()
    for client in clients:
        print(str(await client.getLastCheckinSeconds()))

asyncio.run(main2())