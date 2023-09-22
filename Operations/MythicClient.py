import Client
from mythic import mythic

class MythicClient(Client.Client):
    mythicInstance = None
    displayID = None

    def __init__(self):
        return

    async def initializeMythic(self):
        # Todo: grab apitoken & ip from config
        apitoken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTQ0NDkwMzgsImlhdCI6MTY5NDQzNDYzOCwidXNlcl9pZCI6MSwiYXV0aCI6ImFwaSJ9.LvxS_fIGrc-W4xLswYRwAa3BbMCymoz0DJgddU666Yo"
        mythicInstance = await mythic.login("34.237.94.238", apitoken=apitoken)

    async def executeCommand(self, command, parameters, displayID):
        await mythic.issue_task_and_waitfor_task_output(self.mythicInstance, command, parameters, displayID)