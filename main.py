# 1. Importação de bibliotecas

import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from dotenv import load_dotenv
import psycopg2
import os
import time

from web_scrapping import Scrap # Importa a função de scraping que retorna uma lista de urls
from ai_agent import ParseToAgent # Importa a função de AI Agent para procurar com base no prompt

# 2. Configuração de variáveis de ambiente

load_dotenv()

api_token = os.getenv("GENAI_TOKEN")
db_endpoint = os.getenv("RDS_ENDPOINT")
url = Scrap()

# 3. Coleta o texto de todas as url de notícias

def GeoLocator(adress):
    geolocator = Nominatim(user_agent="roubo_carga_scraper")

    geo_dados = []

    try:
        location = geolocator.geocode(adress)
        if location:
            geo_dados.append({
                "lat": location.latitude,
                "lng": location.longitude,
                "intensity": 4,  # você pode definir a regra
                "type": "Roubo de carga"
                })
    except Exception as e:
        print("Erro geocodificando:", adress, e)
    
    return geo_dados

def Agent(url, api_token):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    texto = " ".join([p.get_text() for p in soup.find_all("p")])

    response = ParseToAgent(texto, api_token)

    return response

conn = psycopg2.connect(
    host=db_endpoint,
    database="news_scrap",
    user="neoroute",
    password="neoroute",
    port=5432,
)

print("Conectado ao banco 'news_scrap' na porta: 5432.")

cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS resultados (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    geo_coord TEXT NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

print("Executando...")

contador = 0

for news_url in url:
    contador += 1

    cur.execute("SELECT 1 FROM resultados WHERE url = %s", (news_url,))
    existe = cur.fetchone()

    if not existe:
        adress = Agent(news_url, api_token)
        geo_coord = GeoLocator(adress)

        cur.execute("INSERT INTO resultados (url, geo_coord) VALUES (%s, %s)",
                (f"{news_url}", f"{geo_coord}"))
        conn.commit()
        print('Dados cadastrados.')
    else:
        print('Url já existe no banco.')
        pass

    if contador % 10 == 0:
        print("\n⏸️ Atingido 10 requisições. Aguardando 60 segundos...")
        time.sleep(60)  # pausa de 1 minuto
        print("▶️ Retomando execução...")

print('Concluído.')

cur.close()
conn.close()

# 2. Geocodificação (OpenStreetMap)
