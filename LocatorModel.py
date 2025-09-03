import requests
from bs4 import BeautifulSoup
import spacy
from geopy.geocoders import Nominatim

# 1. Coleta de uma notícia
url = "https://g1.globo.com/rs/rio-grande-do-sul/noticia/2025/08/10/nove-pessoas-sao-presas-por-roubo-de-carga-de-frango-apos-queda-de-caminhao-em-ponte-no-rs.ghtml"
html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")

texto = " ".join([p.get_text() for p in soup.find_all("p")])


# 2. Extração de local com NLP (spaCy em português)
nlp = spacy.load("pt_core_news_sm")
doc = nlp(texto)

vias_keywords = ["Rodovia", "Rod.", "Rua", "Avenida", "Av.", "Estrada", "Marginal", "BR"]

locais = [ent.text for ent in doc.ents if ent.label_ == "LOC"]
print(locais)
vias = []
for lugar in locais:
    if any(keyword in lugar for keyword in vias_keywords):
        vias.append(lugar)

print(vias)
#print("Locais encontrados:", locais)

# 3. Geocodificação (OpenStreetMap)
geolocator = Nominatim(user_agent="roubo_carga_scraper")

geo_dados = []
for lugar in vias:
    try:
        location = geolocator.geocode(lugar + ", Brasil")
        if location:
            geo_dados.append({
                "lat": location.latitude,
                "lng": location.longitude,
                "intensity": 4,  # você pode definir a regra
                "type": "Roubo de carga"
            })
    except Exception as e:
        print("Erro geocodificando:", lugar, e)

print(geo_dados)
