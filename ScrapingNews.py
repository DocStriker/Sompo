from GoogleNews import GoogleNews
import requests
from bs4 import BeautifulSoup
import requests
import pandas as pd


def searchFromGoogleNews():
    gn = GoogleNews(lang='pt', region='BR', period='7d')
    gn.search("roubo de carga rodovia")

    results = gn.result()

    for r in results:
        print("Título:", r['title'])
        print("Link:", r['link'])
        print("Data:", r['date'])
        print("-" * 80)
    
def searchFromGdelt():
    url = "https://api.gdeltproject.org/api/v2/doc/doc/query?mode=ArtList&format=json&maxrecords=15"
    params = {
        "query": "truck theft sourcecountry:brazil",
    }

    resp = requests.get(url, params=params)
    data = resp.json()

    # Transformar em DataFrame para analisar
    articles = pd.DataFrame(data["articles"])
    print(articles.loc[9]['url'])

if __name__ == "__main__":
    searchFromGoogleNews()