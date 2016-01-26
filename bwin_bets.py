from bs4 import BeautifulSoup
from datetime import datetime, date
from Competition import Competition
from MatchJsonEncoder import MatchJsonEncoder
from Match import Match
import bd
import requests
import json
import logging

logger = logging.getLogger(__name__)


def _get_date(day_elem):
    logger.debug('Start parsing date')
    text = day_elem.text.strip()
    str_date = text[-10:]
    match_date = datetime.strptime(str_date, '%d/%m/%Y').date()
    logger.debug('Finish parsing date: %s', str(match_date))
    return match_date


def _get_match_time(match_elem):
    logger.debug('Start parsing time')
    time_str = match_elem.parent.parent.findNext('h6').text.strip()
    match_time = datetime.strptime(time_str, '%H:%M').time()
    logger.debug('Finish parsin time: %s', str(match_time))
    return match_time


def _get_match_data(match_elem):
    logger.debug('Start parsing match data')
    teams = [option.text for option in match_elem.find_all(class_='option-name') if option.text != 'X']
    mults = [float(odds.text) for odds in match_elem.find_all(class_='odds')]
    match_time = _get_match_time(match_elem)
    logger.debug('Finish parsing match data: %s, %s', teams, mults)
    return teams, mults, match_time


def _get_competition(competition_elem):
    logger.debug('Start parsing competition')
    code = competition_elem.div['data-league']
    name = competition_elem.a.text
    name = ' '.join([name.strip() for name in name.splitlines()])
    comp = Competition(code, name)
    logger.debug('Finish parsing competition: %s', comp)
    return comp


def get_matches(day):
    logger.info('Start scraping matches on: %s', str(day))
    matches_obj = []
    finished = False
    page = 0
    url = 'https://sports.bwin.es/es/sports/indexmultileague'
    post_data = {'sportId': '4', 'page': str(page), 'dateFilter': str(day)}

    while not finished:
        logger.info('Scraping page %d', page)
        request = requests.post(url, post_data)
        soup = BeautifulSoup(request.text, 'html.parser')
        competitions = soup.find_all(class_='event-group-level1')
        logger.info('%d competitions found', len(competitions))
        for competition in competitions:
            comp_obj = _get_competition(competition)
            logger.info('Scraping competition: %s', comp_obj)
            match_listing = competition.parent.findNext('ul')
            matches = match_listing.find_all(class_='col3 three-way')
            logger.info('%d matches found', len(matches))
            for match in matches:
                teams, mults, match_time = _get_match_data(match)
                match_obj = Match(teams[0], teams[1], mults, comp_obj, datetime.combine(day, match_time))
                matches_obj.append(match_obj)
        if len(competitions) == 0:
            finished = True
        page += 1
        post_data['page'] = page
    logger.info('Stop scraping matches on: %s. Matches found: %d', str(day), len(matches_obj))
    return matches_obj

if __name__ == "__main__":
    today = date.today()
    today_matches = get_matches(today)
    today_json_matches = [json.loads(MatchJsonEncoder().encode(m)) for m in today_matches]
    bd.insert_new_matches(today_json_matches)
