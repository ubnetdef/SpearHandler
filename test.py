from Operations import Operation, MythicClient
import asyncio

async def main():
    inScopeIPs = ["192.168.13.28"]
    clients = []

    testOperation = Operation.Operation(inScopeIPs, clients)

    displayID = 123
    startKaliClient = MythicClient.MythicClient(displayID)
    await startKaliClient.initializeMythic()

    testOperation.addClient(startKaliClient)

    await testOperation.startOperation()

asyncio.run(main())