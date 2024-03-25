class SimpleClass:
    def __init__(self, attribute):
        self.attribute = attribute

    def getAttribute(self):
        return self.attribute
    
    def kaboom(self):
        raise Exception("kaboom")