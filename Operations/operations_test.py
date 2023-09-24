from mythic import mythic
import asyncio
import MythicClient
import pytest

pytest_plugins = ('pytest_asyncio',)

@pytest.mark.asyncio
async def test_MythicClientCommand():
    mythicClient = MythicClient.MythicClient(11)
    await mythicClient.initializeMythic()
    print(mythicClient)
    await mythicClient.executeCommand("ls", "", 7)
    assert True

@pytest.mark.asyncio
async def test_MythicClientUpload():
    mythicClient = MythicClient.MythicClient(11)
    await mythicClient.initializeMythic()
    print(mythicClient)
    await mythicClient
    assert True

def test_always_passes():
    assert True