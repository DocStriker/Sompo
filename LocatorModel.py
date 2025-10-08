import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim

from ScrapingNews import Scrap
from AIAgent import ParseToAgent

# 1. Coleta de uma notícia
url = Scrap()[1]

html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")

texto = " ".join([p.get_text() for p in soup.find_all("p")])

response = ParseToAgent(texto)
print(response)

# 3. Geocodificação (OpenStreetMap)
geolocator = Nominatim(user_agent="roubo_carga_scraper")

geo_dados = []

try:
    location = geolocator.geocode(response)
    if location:
        geo_dados.append({
            "lat": location.latitude,
            "lng": location.longitude,
            "intensity": 4,  # você pode definir a regra
            "type": "Roubo de carga"
            })
except Exception as e:
    print("Erro geocodificando:", response, e)

print(geo_dados)
