from bwin_bets import get_matches
from bwin_results import get_matches_results
from datetime import date
from MatchJsonEncoder import MatchJsonEncoder
import json
import bd
import schedule
import time


def store_new_matches():
    today = date.today()
    today_matches = get_matches(today)
    today_json_matches = [json.loads(MatchJsonEncoder().encode(m)) for m in today_matches]
    bd.insert_new_matches(today_json_matches)


def update_results():
    matches_results = get_matches_results()
    for match_result in matches_results:
        bd.update_results(match_result, match_result.result)


def main():
    schedule.every().hour.do(store_new_matches)
    schedule.every(151).minutes.do(store_new_matches)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
