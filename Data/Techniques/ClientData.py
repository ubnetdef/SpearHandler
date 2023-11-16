from Data.Techniques import ServicesData

class ClientData:
    # This design right here of using ipAddresses like a primary key has networking implications I can't think of right now
    def __init__(self, ipAddress):
        self.ipAddress = ipAddress
        self.servicesData: ServicesData.ServicesData = ServicesData.ServicesData()
        # Options:
        # linux, windows, freebsd
        operatingSystem = None