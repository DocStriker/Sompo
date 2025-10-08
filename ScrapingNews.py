from GoogleNews import GoogleNews
import requests
import pandas as pd


def searchFromGoogleNews():
    gn = GoogleNews(lang='pt', region='BR', period='7d')
    gn.search("roubo de carga rodovia")

    links = []
    results = gn.result()

    for r in results:
        links.append(r['link'])

    
    return links
    
def searchFromGdelt():
    url = "https://api.gdeltproject.org/api/v2/doc/doc/query?mode=ArtList&format=json&maxrecords=50&startdatetime=20250101000000&enddatetime=20251007235959"
    params = {
        "query": "truck theft sourcecountry:brazil",
    }

    resp = requests.get(url, params=params)
    data = resp.json()

    links = []
    # Transformar em DataFrame para analisar
    articles = pd.DataFrame(data["articles"])

    for a in range(len(articles)):
        links.append(articles.loc[a]['url'])

    return links

def Scrap():
    link_news = []

    for nlgn in searchFromGoogleNews():
        link_news.append(nlgn)
    for nlgd in searchFromGdelt():
        link_news.append(nlgd)

    return link_news

if __name__ == "__main__":
    for s in Scrap():
        print(s)