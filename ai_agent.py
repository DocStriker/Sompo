from google import genai
from google.genai import types


def ParseToAgent(texto, api_token):

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

if __name__ == '__main__':
    print(ParseToAgent(""))