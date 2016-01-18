from pymongo import MongoClient

client = MongoClient()
db = client.bets
coll = db.matches


def insert_matches(matches):
    coll.insert_many(matches)
