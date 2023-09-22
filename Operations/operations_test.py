from mythic import mythic
import asyncio
import MythicClient

async def test_MythicClientCommand():
    mythicClient = MythicClient.MythicClient()
    await mythicClient.initializeMythic()
    mythicClient.displayId=7
    print(mythicClient)
    await mythicClient.executeCommand("ls", "", 7)
    print("aaaaa")
    assert True
asyncio.run(test_MythicClientCommand())

def test_always_passes():
    assert True