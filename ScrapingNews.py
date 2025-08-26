'''

from GoogleNews import GoogleNews
import requests
from bs4 import BeautifulSoup

url = "https://g1.globo.com/sp/sorocaba-jundiai/noticia/2025/06/18/motorista-de-caminhao-e-feito-refem-por-quase-cinco-horas-durante-assalto-em-rodovia-do-interior-de-sp.ghtml&ved=2ahUKEwjdpdfolqmPAxWsgWEGHUF2G_QQxfQBegQIAhAC&usg=AOvVaw2rdJGfiCuSq4YYzB_xotkU"
html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")

for noticia in soup.find_all("a", class_="feed-post-link"):
    titulo = noticia.get_text()
    link = noticia["href"]
    if "roubo de carga" in  titulo.lower() or "assalto" in titulo.lower():
        print("Título:", titulo)
        print("Link:", link)
        print("-" * 80)
    else:
        print("nada encontrado")
'''
'''

gn = GoogleNews(lang='pt', region='BR', period='7d')
gn.search("roubo de carga rodovia")

results = gn.result()

for r in results:
    print("Título:", r['title'])
    print("Link:", r['link'])
    print("Data:", r['date'])
    print("-" * 80)
    
'''

import requests
import pandas as pd

url = "https://api.gdeltproject.org/api/v2/doc/doc/query?mode=ArtList&format=json&maxrecords=15"
params = {
    "query": "truck theft sourcecountry:brazil",
}

resp = requests.get(url, params=params)
data = resp.json()



# Transformar em DataFrame para analisar
articles = pd.DataFrame(data["articles"])
print(articles.loc[9]['url'])