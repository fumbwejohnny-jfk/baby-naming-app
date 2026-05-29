class Stat:
    def __init__(self, name, gender, yob, ranking):
        self.name = name
        self.gender = gender
        self.yob = yob
        self.ranking = ranking
    
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def gender(self):
        return self._gender
    @gender.setter
    def gender(self, value):
        self._gender = value
    
    @property
    def yob(self):
        return self._yob
    @yob.setter
    def yob(self, value):
        self._yob = value

    @property
    def ranking(self):
        return self._ranking
    @ranking.setter
    def ranking(self, value):
        self._ranking = value