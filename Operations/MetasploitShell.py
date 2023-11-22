from __future__ import annotations
from Operations.Client import *
from pymetasploit3.msfrpc import *
from Attacks.MetasploitAttack import MetasploitAttack
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Attacks.Attack import *
    from Attacks.MetasploitAttack import MetasploitAttack
    from Operation import *

class MetasploitC2():
    def __init__(self, metasploitRPCIP, password, port=55552):
        self.metasploitServer = MsfRpcClient(password, port=port, server=metasploitRPCIP)

    def loadModuleAsAttack(self, module: ExploitModule, operation: Operation):
        newAttack = MetasploitAttack(module, self)
        if(newAttack.onlyRequiresRHOSTS()):
            operation.addAttack(newAttack)
            print("%s module loaded!" % module.info['name'])
        else:
            raise Exception("Unsupported required options in metasploit module")

    def loadExploitAttacks(self, operation: Operation):
        # Note to self
        # - Loads only certain sections of metasploit
        modules = []
        modules += self.metasploitServer.modules.exploits
        for moduleName in modules:
            module = self.metasploitServer.modules.use('exploit', moduleName)
            try:
                self.loadModuleAsAttack(module, operation)
            except Exception as e:
                continue

    def getLatestSessionID(self):
        sessionIDs = self.metasploitServer.sessions.list.keys()
        highestSessionID = -1
        for sessionID in sessionIDs:
            if(sessionID > highestSessionID):
                highestSessionID = sessionID
        if(highestSessionID == -1):
            raise Exception("No sessions found")
        return highestSessionID

    def getLatestSession(self):
        latestSessionID = self.getLatestSessionID()
        client = MetasploitShell(latestSessionID, self)
        return client

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