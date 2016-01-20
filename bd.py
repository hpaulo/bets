from pymongo import MongoClient
from Match import Match

client = MongoClient()
db = client.bets
coll = db.matches


def find_match(mdatetime, local, visitor):
    query = {'mdatetime': mdatetime, 'local': local, 'visitor': visitor}
    match_dict = coll.find_one(query)
    match = Match.from_json(match_dict)
    return match


def insert_new_matches(matches):
    for match_dict in matches:
        match = find_match(match_dict['mdatetime'], match_dict['local'], match_dict['visitor'])
        if match:
            print('Found: ', match)
        else:
            print('NOT FOUND: ', match_dict)
            coll.insert_one(match_dict)
