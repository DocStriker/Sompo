from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()

api_token = os.getenv("GENAI_TOKEN")


def ParseToAgent(texto):

    prompt = f"""
        No texto: {texto},

        Extraia a localização principal mencionada no texto e retorne
        no seguinte formato: "Rodovia/Rua, cidade, estado" """
        

    client = genai.Client(api_key=api_token)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0)  # Disables thinking
        ),
    )
    return response.text
