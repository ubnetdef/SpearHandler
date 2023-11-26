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
    def meetsPrereqs(self, clientData: ClientData):
        metasploitName: str = self.exploitModule.info['name']
        hasMetasploitService: bool = clientData.servicesData.hasServiceNameInMetasploitName(metasploitName)
        return hasMetasploitService
        # for client in clientsWithService:
        #     client.executeAttack(...)

    async def execute(self, targetHost: ClientData, metasploitServer: MetasploitC2, operation: Operation):
        # Known bug/limitation here: Metasploit Exploit Overlap Bug
        # Todo: Data will have to be passed in smartly
        output = self.exploitModule.execute(payload='cmd/unix/interact')
        metasploitShell = metasploitServer.getLatestSession()
        targetHost.c2Shells.append(metasploitShell)