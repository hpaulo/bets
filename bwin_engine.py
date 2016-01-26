from bwin_bets import get_matches
from bwin_results import get_matches_results
from datetime import date
from MatchJsonEncoder import MatchJsonEncoder
import json
import bd
import schedule
import time
import logging


def store_new_matches():
    logger.info('Start scraping and storing new matches')
    today = date.today()
    today_matches = get_matches(today)
    today_json_matches = [json.loads(MatchJsonEncoder().encode(m)) for m in today_matches]
    bd.insert_new_matches(today_json_matches)
    logger.info('Finish scraping and storing new matches')


def update_results():
    logger.info('Start scraping and updating results')
    matches_results = get_matches_results()
    logger.debug('Number of results: %d', len(matches_results))
    for match_result in matches_results:
        bd.update_results(match_result, match_result.result)
    logger.info('Finish scraping and updating results')


def main():
    logger.info('Starting application')
    schedule.every().hour.do(store_new_matches)
    schedule.every(151).minutes.do(store_new_matches)
    logger.info('Starting job scheduler infinite loop')
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    import logging.config
    logging.config.fileConfig('conf/log.conf')
    logger = logging.getLogger(__name__)
    main()
