from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Operations import Client, Operation
from Attacks import Attack
from Data.Techniques import Database
from Data.Techniques import ServiceData
import re

# This is intended to be run on the starting malicious attacker client

class RunNMAP(Attack.Attack):
    # This parsing code is absolutely god awful
    def __parsePortAndProtocol(self, data):
        for i in range(len(data)):
             service = data[i]
             portAndProtocol = service[0]
             split = portAndProtocol.split("/")
             protocol = split[1]
             port = split[0]
             data[i].insert(0, protocol)
             data[i].insert(0, port)
             data[i].pop(2)


    def __parseNMAPToDatatypes(self, nmapOutput):
        pattern = re.compile(r"[0-9]+/[A-Za-z]+\s+[A-Za-z]+\s+[A-Za-z-]+", re.IGNORECASE)
        matched = pattern.findall(nmapOutput) # This needs testing

        for i in range(len(matched)):
                rawPortStateService = matched[i]
                matched[i] = rawPortStateService.split()
                
        return matched

    def __parse(self, rawdata):
        data = self.__parseNMAPToDatatypes(rawdata)
        self.__parsePortAndProtocol(data)
        return data

    # def __inScopeIPsAsString(self, inScopeIPsList):
    #     inScopeString = ""
    #     for ip in inScopeIPsList:
    #         inScopeString += ip + " "

    #     inScopeString = inScopeString.rstrip(" ")
    #     return inScopeString

    def __storeData(self, result, ip):
        for service in result:
            port = service[0]
            protocol = service[1]
            status = service[2]
            name = service[3]
            externallyAccessible = True

            serviceData = ServiceData(name, port, externallyAccessible)

            clientData = Database.Database().getClientData(ip)
            clientData.servicesData.addServiceData(serviceData)

    async def execute(self, client: Client.Client, operation: Operation.Operation):
        for ip in operation.inScopeIPs:
            # This may be a bad implementation as for each ip in scope it executes a mythic command
            result = await client.executeShell("sudo nmap %s" % ip)
            parsed = self.__parse(result)
            self.__storeData(parsed, ip)
            print(parsed)