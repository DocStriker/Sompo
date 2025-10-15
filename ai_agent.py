import requests
from google import genai
from google.genai import types
from bs4 import BeautifulSoup
import os
import json

from dotenv import load_dotenv

load_dotenv()

api_token = os.getenv('GENAI_TOKEN')

def TestingScrap():

    url = 'https://g1.globo.com/mt/mato-grosso/noticia/2025/09/24/roubos-de-carga-de-caminhao-tem-queda-de-mais-de-40percent-com-ajuda-de-tecnologia-em-mt.ghtml'

    html = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text
    soup = BeautifulSoup(html, "html.parser")

    texto = " ".join([p.get_text() for p in soup.find_all("p")])

    return texto

def ParseToAgent(texto, api_token):

    prompt = f"""
        No texto: {texto},

        Extraia a localização principal mencionada no texto e retorne
        no seguinte formato: 
        
        ['street': 'Rodovia/Rua', 'city': 'cidade' ou ''(caso não tenha), 'state': estado (ex: MG), 'cargo_type': tipo de carga roubada em só uma palavra sem acentos e no plural (ex: Eletrônicos, Móveis...)] """
        

    client = genai.Client(api_key=api_token)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0)  # Disables thinking
        ),
    )

    if response.text:
        try:
            data = json.loads(response.text[8:-3])
        except json.JSONDecodeError as e:
            print("Erro ao decodificar JSON:", e)
            data = None

    return data

if __name__ == '__main__':
    texto = TestingScrap()
    print(ParseToAgent(texto, api_token=api_token))