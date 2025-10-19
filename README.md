# 1. Descrição técnica completa — “Projeto API-NeoRoute”
**Nome do Projeto**

>API-NeoRoute – Sistema Inteligente de Monitoramento de Ocorrências Rodoviárias no Brasil

**Objetivo**

>A **API-NeoRoute** tem como objetivo automatizar a coleta, extração e georreferenciação de notícias sobre ocorrências rodoviárias e roubos de carga no Brasil, utilizando IA e serviços em nuvem para gerar uma base de dados estruturada e atualizada em tempo quase real.

**Arquitetura e Pipeline**

**1. Coleta de Dados**

>Utiliza a API do GDELT (Global Database of Events, Language, and Tone) para buscar notícias publicadas nos últimos 3 dias relacionadas a crimes, ocorrências e transporte rodoviário.
>
>As URLs retornadas são armazenadas temporariamente e passam por validação.

**2. Extração de Texto**

>Cada URL é processada pelo BeautifulSoup, que faz web scraping do conteúdo HTML e extrai apenas o texto principal da notícia, removendo anúncios, menus e elementos irrelevantes.

**3. Interpretação Semântica**

>O texto limpo é enviado à API Gemini (Google), que realiza análise semântica para identificar:
>
>- Endereço/local do evento
>
>- Estado brasileiro
>
>- Tipo de carga envolvida
>
>- Data do fato ou publicação

**4. Geocodificação**

>O endereço identificado é georreferenciado via API do Nominatim (OpenStreetMap), que retorna as coordenadas geográficas (latitude e longitude) do local.

**5. Armazenamento e Persistência**

>Os dados estruturados são gravados em um banco relacional AWS RDS (PostgreSQL), contendo:
>
>```id```, ```url```, ```data```, ```estado```, ```coordenadas``` na tabela **'rotas'**.
>
>```id```, ```tipo_carga``` na tabela **'cargas'**.
>
>```id_rotas```, ```id_cargas```, na tabela associativa (N:N) **'rota_cargas'**.
>
>Utilizando as boas práticas de atomização de informações utilizando a **Primeira Forma Normal (1FN)** na normalização de banco de dados.

**6. Exposição via API REST**

>O backend é uma API FastAPI autenticada por API Token, permitindo:
>
>- Consulta de registros filtrados por data, estado ou tipo de carga.
>
>- Inserção automática de novos eventos a partir do pipeline.
>
>- Endpoint de saúde (/docs) e documentação interativa via Swagger.

**7. Infraestrutura e Deploy**

>Contêinerizado com Docker, imagens armazenadas no AWS ECR (Elastic Container Registry).
>
>Implantação orquestrada via AWS ECS (Elastic Container Service).
>
>Balanceamento de carga e HTTPS configurados via AWS Application Load Balancer.
>
>Logs e monitoramento integrados ao AWS CloudWatch.

**Tecnologias Utilizadas**

|Categoria |	Ferramentas|
| --------- |  --------- |
|Linguagem |	Python 3.11|
|Framework Web |	FastAPI|
|IA / NLP	Google | Gemini API|
|Coleta de Dados |	GDELT API, BeautifulSoup|
|Geolocalização |	Nominatim (OpenStreetMap)|
|Banco de Dados |	AWS RDS (PostgreSQL)|
|Containerização |	Docker|
|Orquestração e Deploy |	AWS ECS, AWS ECR|
|Infraestrutura de Rede |	AWS Load Balancer|
|Monitoramento |	AWS CloudWatch|
|Autenticação |	API Token|
|Controle de Versão |	Git + GitHub|

**Fluxo de Dados Resumido**
```
GDELT
→ URLs
→ BeautifulSoup
→ Texto limpo
→ Gemini
→ Endereço + Estado + Tipo de Carga + Data
→ Nominatim
→ Coordenadas
→ RDS (PostgreSQL)
→ FastAPI
→ ECS + Load Balancer (HTTPS)
```
**Classificação do Sistema**

>O NeoRoute é classificado como uma API de Inteligência de Dados e Geolocalização,
com pipeline automatizado e componentes de IA — um serviço inteligente parcialmente autônomo (proto-agente).

**Possíveis Extensões Futuras**

>Treinamento de modelo próprio de NER (Named Entity Recognition) para extrair localizações com mais precisão.
>
>Dashboard interativo com Streamlit ou Plotly Dash para mapear as ocorrências.
>
>Criação de um agente autônomo de monitoramento, que decide quando e onde buscar novas notícias conforme padrões de roubo de carga.
