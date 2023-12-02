from __future__ import annotations
from Operations.Client import *
from pymetasploit3.msfrpc import *
from Attacks.MetasploitAttack import MetasploitAttack
from typing import TYPE_CHECKING
import pickle
if TYPE_CHECKING:
    from Attacks.Attack import *
    from Attacks.MetasploitAttack import MetasploitAttack
    from Operation import *

# Uses singleton
class MetasploitModuleCache():
    instance = None

    def getInstance(self):
        if(self.instance == None):
            self.instance = self
        return self.instance
    
    # Overwrites file
    def cacheExploitModules(self, modules: list[ExploitModule]):
        file = open("./exploit-modules-cache.pickle", "wb+")
        pickle.dump(modules, file)

    def cacheExploitModule(self, module: ExploitModule):
        exploitModules: list[ExploitModule] = self.getCachedExploitModules()
        exploitModules.append(module)
        self.cacheExploitModules(exploitModules)
    
    def getCachedExploitModules(self):
        try:
            file = open("./exploit-modules-cache.pickle", "rb")
            metasploitCache = pickle.load(file)
            return metasploitCache
        except FileNotFoundError:
            return []
        except EOFError:
            return []

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

    def loadExploitAttacksFromCache(self, operation: Operation):
        moduleCache = MetasploitModuleCache().getInstance()
        exploitCache = moduleCache.getCachedExploitModules()

        if(len(exploitCache) == 0):
            raise Exception("No cahce")
        
        for module in exploitCache:
            try:
                self.loadModuleAsAttack(module, operation)
            except Exception as e:
                continue

    def loadExploitAttacks(self, operation: Operation):
        try:
            self.loadExploitAttacksFromCache(operation)
        except Exception:
            self.loadExploitAttacksFromServer(operation)
            
        

    def loadExploitAttacksFromServer(self, operation: Operation):
        # Note to self
        # - Loads only certain sections of metasploit
        # Todo: change this to load into cache
        modules = []
        modules += self.metasploitServer.modules.exploits
        for moduleName in modules:
            module = self.metasploitServer.modules.use('exploit', moduleName)
            cache = MetasploitModuleCache().getInstance()
            cache.cacheExploitModule(module)
            try:
                self.loadModuleAsAttack(module, operation)
            except Exception as e:
                continue

    def getLatestSessionID(self):
        sessionIDs = self.metasploitServer.sessions.list.keys()
        highestSessionID = -1
        for sessionID in sessionIDs:
            if(int(sessionID) > highestSessionID):
                highestSessionID = int(sessionID)
        if(highestSessionID == -1):
            raise Exception("No sessions found")
        return highestSessionID

    def getLatestSession(self, ipAddress):
        latestSessionID = self.getLatestSessionID()
        client = MetasploitShell(latestSessionID, self, ipAddress)
        return client

    def runCommandOnSession(self, sessionID, command):
        session = self.metasploitServer.sessions.session(str(sessionID))
        session.write(command)
        output = session.read().rstrip("\n")
        return output

class MetasploitShell(C2Client):
    def __init__(self, sessionID: int, metasploitServer: MetasploitC2, ipAddress=None):
        id = None
        self.ipAddress = ipAddress
        self.sessionID = sessionID
        self.metasploitServer = metasploitServer

    async def getIPAddress(self):
        return self.ipAddress

    def executeShell(self, command):
        return self.metasploitServer.runCommandOnSession(self.sessionID, command)