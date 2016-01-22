from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import locale
import re
import bd


def _parse_results(result_text):
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


def _parse_teams(teams_text):
    teams_splitted = teams_text.split(' - ')
    local_team = teams_splitted[0].strip()
    visitor_team = teams_splitted[1].strip()
    if visitor_team.endswith('(Campo neutral)'):
        visitor_team = visitor_team[:-16]
    return local_team, visitor_team


def _parse_date(date_text):
    parsed_date = datetime.strptime(date_text, '%A, %d de %B de %Y').date()
    return parsed_date


def _parse_time(time_text):
    parsed_time = datetime.strptime(time_text, '%H:%M').time()
    return parsed_time


def get_matches_results():
    locale.setlocale(locale.LC_ALL, 'Spanish')
    matches = []
    finished = False
    page = 0
    url = 'https://sports.bwin.es/es/sports/results?sport=4&period=ThreeDays&sort=Date&page='
    while not finished:
        r = requests.get(url + str(page))
        soup = BeautifulSoup(r.text, 'html.parser')
        date_elems = soup.find_all(class_='result-group date')
        for date_elem in date_elems:
            mdate = _parse_date(date_elem.h3.text.strip())
            competition_elems = soup.find_all(class_='result-subgroup league')
            for competition_elem in competition_elems:
                match_elems = competition_elem.tbody.find_all('tr')
                for match_elem in match_elems:
                    name_elem = match_elem.find(class_='name')
                    result_elem = match_elem.find(class_='result')
                    time_elem = match_elem.find(class_='time')
                    local, visitor = _parse_teams(name_elem.text)
                    result = _parse_results(result_elem.text)
                    mtime = _parse_time(time_elem.text)
                    # UTC is used for results, Spain timezone for bets
                    mdatetime = datetime.combine(mdate, mtime) + timedelta(hours=1)
                    match = bd.find_match(str(mdatetime), local, visitor)
                    if not match:
                        print('NOT FOUND!', mdatetime, local, visitor)
                    else:
                        match.result = result
                        matches.append(match)
        if len(date_elems) == 0:
            finished = True
        page += 1
    return matches


if __name__ == "__main__":
    matches_results = get_matches_results()
    for match_result in matches_results:
        print(match_result, match_result.result)
        bd.update_results(match_result, match_result.result)
