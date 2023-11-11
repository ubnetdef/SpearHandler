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

# This is intended to be run on the starting malicious attacker client

class RunNMAP(Attack.Attack):

    def __parseToServiceData(self, rawdata):
        xmlParsed = ET.fromstring(rawdata)
        hostsXML = xmlParsed.findall("./host")
        clientsData = ClientsData()
        for hostXML in hostsXML:
            portsXML = hostXML.findall("./ports/port")
            addressXML = hostXML.findall("./address")
            address = addressXML[0].attrib['addr']
            clientData = ClientData(address)
            for portXML in portsXML:
                portNumber = portXML.attrib["portid"]
                servicesXML = portXML.findall("./service")
                for serviceXML in servicesXML:
                    serviceName = serviceXML.attrib.get('product','')
                    serviceType = serviceXML.attrib['name']
                    serviceData = ServiceData(name=serviceName, type=serviceType, port=portNumber, externallyAccessible=True)
                    clientData.servicesData.addServiceData(serviceData)
            clientsData.addClientData(clientData)
        return clientsData

    def __storeData(self, operation: Operation.Operation, clientsData: ClientsData):
        operation.clientsData.mergeClientData(clientsData)

    async def execute(self, client: Client.Client, operation: Operation.Operation):
        print(operation.inScopeIPs)
        # This may be a bad implementation as for each ip in scope it executes a mythic command
        xmlPath = "/root/scan" + str(uuid.uuid4()) + ".xml"
        await client.executeShell("sudo nmap -sV -oX %s %s" % (xmlPath, ' '.join(operation.inScopeIPs)))
        result = await client.executeShell("cat %s" % xmlPath)
        parsed = self.__parseToServiceData(result)
        self.__storeData(operation, parsed)
        print(parsed)