from Operations import Client
from mythic import mythic

class MythicClient(Client.Client):
    mythicInstance = None
    displayID = None

    def __init__(self, displayID):
        self.displayID = displayID

    async def initializeMythic(self):
        # Todo: grab apitoken & ip from config
        apitoken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTQ0NDkwMzgsImlhdCI6MTY5NDQzNDYzOCwidXNlcl9pZCI6MSwiYXV0aCI6ImFwaSJ9.LvxS_fIGrc-W4xLswYRwAa3BbMCymoz0DJgddU666Yo"
        self.mythicInstance = await mythic.login("34.237.94.238", apitoken=apitoken)

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