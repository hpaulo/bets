from pymongo import MongoClient
from Match import Match
import logging

logger = logging.getLogger(__name__)

client = MongoClient()
db = client.bets
coll = db.matches


def find_match(mdatetime, local, visitor):
    logger.debug('Start finding match: %s, %s, %s', mdatetime, local, visitor)
    query = {'mdatetime': mdatetime, 'local': local, 'visitor': visitor}
    match_dict = coll.find_one(query)
    match = Match.from_json(match_dict)
    logger.debug('Stop finding match: %s', match)
    return match


def insert_new_matches(matches):
    logger.debug('Start inserting new matches')
    for match_dict in matches:
        match = find_match(match_dict['mdatetime'], match_dict['local'], match_dict['visitor'])
        if match:
            logger.debug('Match already in database')
        else:
            logger.debug('New match: %s', match_dict)
            coll.insert_one(match_dict)
    logger.debug('Finish inserting new matches %d', len(matches))


def update_results(match, result):
    logger.debug('Start updating match results: %s, %s', match, result)
    coll.update_one({'mdatetime': str(match.mdatetime), 'local': match.local, 'visitor': match.visitor},
                    {'$set': {'result': result}})
    logger.debug('Finish updating match results')
