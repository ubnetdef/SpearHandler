from Data.Techniques import ServicesData

class ClientData:
    ipAddress = ""
    servicesData: ServicesData.ServicesData = None
    
    # This design right here of using ipAddresses like a primary key has networking implications I can't think of right now
    def __init__(self, ipAddress):
        self.ipAddress = ipAddress