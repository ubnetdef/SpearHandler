from mythic import mythic
import asyncio
import MythicClient
import pytest

pytest_plugins = ('pytest_asyncio',)

@pytest.mark.asyncio
async def test_MythicClientCommand():
    mythicClient = MythicClient.MythicClient()
    await mythicClient.initializeMythic()
    mythicClient.displayId=7
    print(mythicClient)
    await mythicClient.executeCommand("ls", "", 7)
    assert True

def test_always_passes():
    assert True