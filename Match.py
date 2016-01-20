from datetime import datetime
from Competition import Competition


class Match:
    def __init__(self, local, visitor, mults, competition, mdatetime=datetime.today()):
        self.local = local
        self.visitor = visitor
        self.mults = mults
        self.competition = competition
        self.mdatetime = mdatetime
        self.result = []

    def __str__(self):
        return str(self.mdatetime) + ': ' + self.local + ' - ' + self.visitor + ' ' + str(self.mults)

    @classmethod
    def from_json(cls, dct):
        if dct is None:
            return None
        competition = Competition(dct['competition']['code'], dct['competition']['name'])
        mdatetime = datetime.strptime(dct['mdatetime'], '%Y-%m-%d %H:%M:%S')
        match = cls(dct['local'], dct['visitor'], dct['mults'], competition, mdatetime)
        match.result = dct['result']
        return match
