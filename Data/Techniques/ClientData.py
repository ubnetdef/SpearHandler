from Data.Techniques import ServicesData

class ClientData:
    # This design right here of using ipAddresses like a primary key has networking implications I can't think of right now
    def __init__(self, ipAddress, c2Client=None):
        self.ipAddress = ipAddress
        self.servicesData: ServicesData.ServicesData = ServicesData.ServicesData()
        self.c2Client = c2Client
        # Options:
        # linux, windows, freebsd
        operatingSystem = None