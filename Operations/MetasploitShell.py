from Client import *
from pymetasploit3.msfrpc import *

class MetasploitC2():
    def __init__(self, metasploitRPCIP, password, port=55552):
        self.metasploitServer = MsfRpcClient(password, port=port, server=metasploitRPCIP)

    def runCommandOnSession(self, sessionID, command):
        session = self.metasploitServer.client.sessions.session(self.sessionID)
        session.write(command)
        return session.read()

class MetasploitShell(Client):
    def __init__(self, sessionID: int, metasploitServer: MetasploitC2):
        id = None
        ipAddress = None
        self.sessionID = sessionID
        self.metasploitServer = metasploitServer

    def executeShell(self, command):
        self.metasploitServer.runCommandOnSession(self.sessionID, command)