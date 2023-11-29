class ServiceData:
    
    def __init__(self, name=None, type=None, port=None, externallyAccessible=None):
        self.name: str = name
        self.type = type
        self.port = port
        self.externallyAccessible = externallyAccessible