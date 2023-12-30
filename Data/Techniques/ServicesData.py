from __future__ import annotations
from typing import TYPE_CHECKING
from typing import List
from Data.Techniques.ServiceData import ServiceData
if TYPE_CHECKING:
    from Data.Techniques.ServicesData import ServicesData

class ServicesData:
    def __init__(self):
        self.services: List[ServiceData] = []

    def getServicesData(self):
        return self.services
    
    def addServiceData(self, serviceData: ServiceData):
        self.services.append(serviceData)

    def hasServiceNameInMetasploitName(self, metasploitName: str):
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