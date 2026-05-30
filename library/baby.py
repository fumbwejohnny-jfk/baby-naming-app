class Baby:
    def __init__(self, name, meaning):
        self.name = name
        self.meaning = meaning
        

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def meaning(self):
        return self._meaning
    @meaning.setter
    def meaning(self, value):
        self._meaning = value
    
   