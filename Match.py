from datetime import datetime


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
