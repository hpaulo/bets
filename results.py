from bs4 import BeautifulSoup
import requests

r = requests.get('https://sports.bwin.es/es/sports/results?sport=4&region=28&league=16109&period=ThreeDays')
soup = BeautifulSoup(r.text, 'html.parser')
print(soup.prettify())
