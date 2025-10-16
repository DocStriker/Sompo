# Imagem base leve
FROM python:3.11-slim

# Define diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos do projeto
COPY . /app

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta onde a API roda
EXPOSE 8000

# Comando para rodar o servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

