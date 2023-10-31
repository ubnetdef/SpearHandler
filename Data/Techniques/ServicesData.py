from typing import List
from Data.Techniques import ServiceData

class ServicesData:
    services: List[ServiceData.ServiceData] = []
    
    def addServiceData(self, serviceData: ServiceData.ServiceData):
        self.services.append(serviceData)