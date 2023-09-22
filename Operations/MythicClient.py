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
        self.mythicInstance = await mythic.login("34.237.94.238", apitoken=apitoken)

    async def executeCommand(self, command, parameters, displayID):
        await mythic.issue_task_and_waitfor_task_output(self.mythicInstance, command, parameters, displayID)

    # Agent downloads from mythic server
    # Note:
    # - Mythic agent must have LS capabilities (not shell command LS, but LS built into mythic) to see files using mythic built-in function
    # (We could code our method via parsing shell ls output but ew)
    # - LS command in mythic can NOT recursively list files, therefore must either know path or code our own recursion
    async def uploadAndRunPayload(self, payload, runCommand):
        raise NotImplementedError
        # TODO