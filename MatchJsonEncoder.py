from json import JSONEncoder


class MatchJsonEncoder(JSONEncoder):
    def default(self, match):
        comp_dict = {'code': match.competition.code, 'name': match.competition.name}
        match_dict = {'local': match.local, 'visitor': match.visitor, 'mdatetime': str(match.mdatetime),
                      'mults': match.mults, 'result': match.result, 'competition': comp_dict}
        return match_dict
