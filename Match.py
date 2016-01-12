from datetime import date


class Match:
    def __init__(self, local, visitor, mults, competition, mdate=date.today()):
        self.local = local
        self.visitor = visitor
        self.mults = mults
        self.competition = competition
        self.mdate = mdate
        self.result = []

    def __str__(self):
        return str(self.mdate) + ': ' + self.local + ' - ' + self.visitor + ' ' + str(self.mults)
