from bs4 import BeautifulSoup
from datetime import datetime
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


r = requests.get('https://sports.bwin.es/es/sports/4/24715/apuestas/primera-divisi%c3%b3n-(liga-bbva)')
soup = BeautifulSoup(r.text, 'html.parser')
days = soup.find_all(class_='event-group-level1')
for day in days:
    print(get_date(day))
    match_listing = day.parent.findNext('ul')
    matches = match_listing.find_all(class_='col3 three-way')
    for match in matches:
        print(get_match_data(match))
