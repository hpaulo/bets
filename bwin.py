from bs4 import BeautifulSoup
from datetime import datetime
from Competition import Competition
from Match import Match
import requests


def get_date(day_elem):
    text = day_elem.text.strip()
    str_date = text[-10:]
    match_date = datetime.strptime(str_date, '%d/%m/%Y').date()
    return match_date


def get_match_data(match_elem):
    teams = [option.text for option in match_elem.find_all(class_='option-name') if option.text != 'X']
    mults = [float(odds.text) for odds in match_elem.find_all(class_='odds')]
    return teams, mults


def get_competition(competition_elem):
    code = competition_elem.div['data-league']
    name = competition_elem.a.text
    name = ' '.join([name.strip() for name in name.splitlines()])
    comp = Competition(code, name)
    return comp


r = requests.get('https://sports.bwin.es/es/sports/4/apuestas/f%c3%batbol/2016-01-11')
soup = BeautifulSoup(r.text, 'html.parser')
competitions = soup.find_all(class_='event-group-level1')
for competition in competitions:
    comp_obj = get_competition(competition)
    print(comp_obj)
    match_listing = competition.parent.findNext('ul')
    matches = match_listing.find_all(class_='col3 three-way')
    for match in matches:
        teams, mults = get_match_data(match)
        match_obj = Match(teams[0], teams[1], mults, comp_obj)
        print(match_obj)
