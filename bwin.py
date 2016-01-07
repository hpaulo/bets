from bs4 import BeautifulSoup
import requests
r = requests.get('https://sports.bwin.es/es/sports/4/24715/apuestas/primera-divisi%c3%b3n-(liga-bbva)')
soup = BeautifulSoup(r.text, 'html.parser')
print soup.prettify()
