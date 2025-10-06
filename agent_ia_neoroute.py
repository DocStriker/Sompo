from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()

api_token = os.getenv("GENAI_TOKEN")

client = genai.Client(api_key=api_token)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Na notícia 'Na madrugada de segunda-feira, criminosos atacaram um caminhão na Rodovia Presidente Dutra', próximo a Guarulhos. O motorista foi abandonado em uma rua do bairro Vila Maria, em São Paulo.', onde ocorreu o crime?",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
    ),
)
print(response.text)