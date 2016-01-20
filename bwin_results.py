from bs4 import BeautifulSoup
from datetime import datetime
import requests
import locale
import re

locale.setlocale(locale.LC_ALL, 'Spanish')
enlace = 'https://sports.bwin.es/es/sports/results?sport=4&period=ThreeDays&sort=Date&page='


def parse_results(result_text):
    hyphen_re = re.compile(r'^(\d+)-(\d+)$')
    colon_re = re.compile(r'^(\d+):(\d+) \(\d+:\d+\)$')
    hyphen_m = hyphen_re.search(result_text)
    colon_m = colon_re.search(result_text)
    if hyphen_m:
        return [int(hyphen_m.group(1)), int(hyphen_m.group(2))]
    elif colon_m:
        return [int(colon_m.group(1)), int(colon_m.group(2))]
    else:
        return []


def parse_teams(teams_text):
    teams_splitted = teams_text.split(' - ')
    return [teams_splitted[0].strip(), teams_splitted[1].strip()]


def parse_date(date_text):
    parsed_date = datetime.strptime(date.h3.text.strip(), '%A, %d de %B de %Y').date()
    return parsed_date


for i in range(6):
    r = requests.get(enlace + str(i))
    soup = BeautifulSoup(r.text, 'html.parser')
    for date in soup.find_all(class_='result-group date'):
        print(parse_date(date.h3.text.strip()))
        competitions = soup.find_all(class_='result-subgroup league')
        for competition in competitions:
            print(competition.thead.tr.th.text.strip())
            matches = competition.tbody.find_all('tr')
            for match in matches:
                name = match.find(class_='name')
                result = match.find(class_='result')
                print(parse_teams(name.text), parse_results(result.text))
