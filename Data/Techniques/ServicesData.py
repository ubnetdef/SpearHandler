from typing import List
from Data.Techniques import ServiceData, ServicesData

class ServicesData:
    def __init__(self):
        self.services: List[ServiceData.ServiceData] = []

    def getServicesData(self):
        return self.services
    
    def addServiceData(self, serviceData: ServiceData.ServiceData):
        self.services.append(serviceData)

    def hasServiceNameInMetasploitName(self, metasploitName: str):
        # Todo: THIS CODE RIGHT BELOW IS A BUGGY DEBUG, REMOVE IT
        if("apache_normalize" in metasploitName):
            return True

        for service in self.services:
            if(service.name.lower() in metasploitName.lower() and service.name != ''):
                return True;
        return False

    def mergeServicesData(self, newServicesData: ServicesData):
        for newServiceData in newServicesData:
            exists = False
            for service in self.services:
                if(service.name == newServiceData.name):
                    exists = True
            
            if(not exists):
                self.services.append(newServiceData)