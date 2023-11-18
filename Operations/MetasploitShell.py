from Operations.Client import *
from pymetasploit3.msfrpc import *
from Attacks.Attack import *
from Attacks.MetasploitAttack import *

class MetasploitC2():
    def __init__(self, metasploitRPCIP, password, port=55552):
        self.metasploitServer = MsfRpcClient(password, port=port, server=metasploitRPCIP)

    def loadMetasploitAsAttack(self, moduleName):
        exploit = self.metasploitServer.modules.use('exploit', moduleName)
        newAttack = MetasploitAttack(exploit)

    def loadAttacks(self):
        # Note to self
        # - Loads only certain sections of metasploit
        modules = []
        modules += self.metasploitServer.modules.exploits
        testmodule = modules[0]
        print(testmodule)
        print(testmodule.options)
        print(modules)

    def runCommandOnSession(self, sessionID, command):
        session = self.metasploitServer.sessions.session(str(sessionID))
        session.write(command)
        output = session.read()
        return output

class MetasploitShell(Client):
    def __init__(self, sessionID: int, metasploitServer: MetasploitC2):
        id = None
        ipAddress = None
        self.sessionID = sessionID
        self.metasploitServer = metasploitServer

    def executeShell(self, command):
        return self.metasploitServer.runCommandOnSession(self.sessionID, command)