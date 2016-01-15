from bs4 import BeautifulSoup
from datetime import datetime
import requests
import locale

locale.setlocale(locale.LC_ALL, 'Spanish')

enlace = 'https://sports.bwin.es/es/sports/results?sport=4&period=ThreeDays&sort=Date&page='

for i in range(6):
    r = requests.get(enlace + str(i))
    soup = BeautifulSoup(r.text, 'html.parser')
    for date in soup.find_all(class_='result-group date'):
        print(datetime.strptime(date.h3.text.strip(), '%A, %d de %B de %Y').date())
        competitions = soup.find_all(class_='result-subgroup league')
        for competition in competitions:
            print(competition.thead.tr.th.text.strip())
            matches = competition.tbody.find_all('tr')
            for match in matches:
                name = match.find(class_='name')
                result = match.find(class_='result')
                print(name.text, result.text)
