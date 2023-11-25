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
    def __parsePortXML(self, portXML):
        portNumber = portXML.attrib["portid"]
        servicesXML = portXML.findall("./service")
        return portNumber, servicesXML

    def __parseNMAPXMLToHostsXML(self, rawXMLString):
        xmlObject = ET.fromstring(rawXMLString)
        HOSTS_XML_PATH = "./host"
        hostsXML = xmlObject.findall(HOSTS_XML_PATH)
        return hostsXML

    def __parseHostXML(self, hostXML):
        portsXML = hostXML.findall("./ports/port")
        addressXML = hostXML.findall("./address")
        address = addressXML[0].attrib['addr']
        return portsXML, address
    
    def __parseServiceXMLToServiceData(self, serviceXML, portNumber):
        serviceName = serviceXML.attrib.get('product','')
        serviceType = serviceXML.attrib['name']
        serviceData = ServiceData(name=serviceName, type=serviceType, port=portNumber, externallyAccessible=True)
        return serviceData

    def __parseNMAPXMLToServiceData(self, rawdata):
        hostsXML = self.__parseNMAPXMLToHostsXML(rawdata)
        clientsData = ClientsData()
        for hostXML in hostsXML:
            portsXML, address = self.__parseHostXML(hostXML)
            clientData = ClientData(address)
            for portXML in portsXML:
                portNumber, servicesXML = self.__parsePortXML(portXML)
                for serviceXML in servicesXML:
                    serviceData = self.__parseServiceXMLToServiceData(serviceXML, portNumber)
                    clientData.servicesData.addServiceData(serviceData)
            clientsData.addClientData(clientData)
        return clientsData

    def __storeData(self, operation: Operation.Operation, clientsData: ClientsData):
        operation.clientsData.mergeClientData(clientsData)

    async def execute(self, client: Client.C2Client, operation: Operation.Operation):
        print(operation.inScopeIPs)
        # This may be a bad implementation as for each ip in scope it executes a mythic command
        xmlPath = "/root/scan" + str(uuid.uuid4()) + ".xml"
        await client.executeShell("sudo nmap -sV -oX %s %s" % (xmlPath, ' '.join(operation.inScopeIPs)))
        result = await client.executeShell("cat %s" % xmlPath)
        parsed = self.__parseNMAPXMLToServiceData(result)
        self.__storeData(operation, parsed)
        print(parsed)