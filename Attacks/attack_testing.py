from mythic import mythic
import asyncio
from Operations import MythicClient
import pytest

pytest_plugins = ('pytest_asyncio',)

@pytest.mark.asyncio
async def RegKeyAttack():
    mythicClient = MythicClient.MythicClient(11)
    await mythicClient.initializeMythic()
    print(mythicClient)
    await mythicClient.executeCommand("ls", "", 7)
    assert True

@pytest.mark.asyncio
async def test_MythicClientUpload():
    mythicClient = MythicClient.MythicClient(16)
    await mythicClient.initializeMythic()
    print(mythicClient)
    await mythicClient.upload_file(b"test", "C:/Users/Blake/Desktop/test1")
    await mythicClient.upload_file(b"test2", "C:/Users/Blake/Desktop/test2")

    assert True

asyncio.run(test_MythicClientUpload())

def test_always_passes():
    assert True