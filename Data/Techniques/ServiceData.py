class ServiceData:
    name = None
    port = None
    externallyAccessible = None
    
    def __init__(self, name, port, externallyAccessible):
        self.name = name
        self.port = port
        self.externallyAccessible = externallyAccessible