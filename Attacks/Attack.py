class Attack:
    def __init__(self, name):
        self.name = name
    def execute(self):
        raise NotImplementedError("execute in attack not implemented!")