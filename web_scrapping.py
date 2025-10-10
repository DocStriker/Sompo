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
    #gnews_links = searchFromGoogleNews()
    gdelt_links = searchFromGdelt()

    '''for nlgn in gnews_links:
        if '&ved' in nlgn:
            url_limpa = nlgn.split('&ved')[0]
            link_news.append(url_limpa)
        else:
            link_news.append(nlgn)'''
    for nlgd in gdelt_links:
        link_news.append(nlgd)

    return set(link_news)

if __name__ == "__main__":
    for s in Scrap():
        print(s)