from bs4 import BeautifulSoup
from datetime import datetime, date
from Competition import Competition
from MatchJsonEncoder import MatchJsonEncoder
from Match import Match
import requests


def _get_date(day_elem):
    text = day_elem.text.strip()
    str_date = text[-10:]
    match_date = datetime.strptime(str_date, '%d/%m/%Y').date()
    return match_date


def _get_match_data(match_elem):
    teams = [option.text for option in match_elem.find_all(class_='option-name') if option.text != 'X']
    mults = [float(odds.text) for odds in match_elem.find_all(class_='odds')]
    return teams, mults


def _get_competition(competition_elem):
    code = competition_elem.div['data-league']
    name = competition_elem.a.text
    name = ' '.join([name.strip() for name in name.splitlines()])
    comp = Competition(code, name)
    return comp


def get_matches(day):
    matches = []
    finished = False
    page = 0
    url = 'https://sports.bwin.es/es/sports/indexmultileague'
    post_data = {'sportId': '4', 'page': str(page), 'dateFilter': str(day)}

    while not finished:
        request = requests.post(url, post_data)
        soup = BeautifulSoup(request.text, 'html.parser')
        competitions = soup.find_all(class_='event-group-level1')
        for competition in competitions:
            comp_obj = _get_competition(competition)
            print(comp_obj)
            match_listing = competition.parent.findNext('ul')
            matches = match_listing.find_all(class_='col3 three-way')
            for match in matches:
                teams, mults = _get_match_data(match)
                match_obj = Match(teams[0], teams[1], mults, comp_obj)
                matches.append(match_obj)
                print(MatchJsonEncoder().encode(match_obj))
        if len(competitions) == 0:
            finished = True
        page += 1
        post_data['page'] = page
    return matches

if __name__ == "__main__":
    today = date.today()
    get_matches(today)
