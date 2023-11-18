from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Operations import Client, Operation
from Attacks import Attack
from Data.Techniques import Database
from Data.Techniques.ServiceData import ServiceData
from Data.Techniques.ClientData import ClientData
import re
import uuid
import xml.etree.ElementTree as ET
from Data.Techniques.ClientsData import ClientsData
from pymetasploit3.msfrpc import *

# This is intended to be run on the starting malicious attacker client

class MetasploitAttack(Attack.Attack):
    # Todo: parse out and store the version

    def __init__(self, module: ExploitModule):
        self.module = module

    async def execute(self, client: Client.Client, operation: Operation.Operation):
        # how tf do we know who to execute it against