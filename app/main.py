from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from agent_task import main

load_dotenv()

db_endpoint = os.getenv('RDS_ENDPOINT')

app = FastAPI()

origins = [
    "http://localhost:3000" # Front local (React, por exemplo   # Seu domínio real (produção)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Quem pode acessar a API
    allow_credentials=True,
    allow_methods=["*"],              # Quais métodos (GET, POST, etc.)
    allow_headers=["*"],              # Quais cabeçalhos podem ser enviados
)

def get_connection():
    return psycopg2.connect(
        dbname="news_scrap",
        user="neoroute",
        password="neoroute",
        host=db_endpoint,
        port="5432"
    )

async def run_agent_task():
    main()
    # por exemplo, scrape + inserção no banco
    await asyncio.sleep(3)  # simula tempo de execução
    return {"status": "Agent executado com sucesso"}

@app.post("/run_agent")
async def run_agent():
    try:
        result = await run_agent_task()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/total/{table_name}")
def total_records(table_name: str):
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(f"SELECT COUNT(*) AS total FROM {table_name};")
        total = cur.fetchone()["total"]
        return {"table": table_name, "total_records": total}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cur.close()
        conn.close()

@app.get("/top_state/{table_name}")
def top_state(table_name: str):
    """
    Retorna o estado com maior número de registros.
    A tabela deve conter uma coluna chamada 'state'.
    """
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query = f"""
            SELECT state, COUNT(*) AS total
            FROM {table_name}
            GROUP BY state
            ORDER BY total DESC
            LIMIT 1;
        """
        cur.execute(query)
        result = cur.fetchone()
        if result:
            return {"top_state": result["state"], "total_records": result["total"]}
        else:
            return {"message": "Nenhum registro encontrado."}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cur.close()
        conn.close()

@app.get("/states/{table_name}")
def top_state(table_name: str):
    """
    Retorna o estado com maior número de registros.
    A tabela deve conter uma coluna chamada 'state'.
    """
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query = f"""
            SELECT state, COUNT(*) AS total
            FROM {table_name}
            GROUP BY state;
        """
        cur.execute(query)
        result = cur.fetchall()
        if result:
            return result
        else:
            return {"message": "Nenhum registro encontrado."}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cur.close()
        conn.close()

@app.get("/top_carga")
def top_carga():
    """Retorna a carga mais recorrente (com mais registros associados)."""
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query = """
            SELECT c.nome AS carga, COUNT(rc.rota_id) AS total
            FROM rota_cargas rc
            JOIN cargas c ON rc.carga_id = c.id
            GROUP BY c.nome
            ORDER BY total DESC
            LIMIT 1;
        """
        cur.execute(query)
        result = cur.fetchone()
        if result:
            return {"top_carga": result["carga"], "total_registros": result["total"]}
        else:
            return {"message": "Nenhum registro encontrado."}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cur.close()
        conn.close()

@app.get("/cargas")
def top_carga():
    """Retorna a carga mais recorrente (com mais registros associados)."""
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query = """
            SELECT c.nome AS carga, COUNT(rc.rota_id) AS total
            FROM rota_cargas rc
            JOIN cargas c ON rc.carga_id = c.id
            GROUP BY c.nome;
        """
        cur.execute(query)
        result = cur.fetchall()
        if result:
            return result
        else:
            return {"message": "Nenhum registro encontrado."}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cur.close()
        conn.close()

# 🔹 Rota 4 — Ocorrências por dia
@app.get("/roubos_por_dia")
def ocorrencias_por_dia():
    """Retorna o número de ocorrências (rotas) por dia."""
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query = """
            SELECT date, COUNT(*) AS total
            FROM rotas
            GROUP BY date
            ORDER BY date ASC;
        """
        cur.execute(query)
        results = cur.fetchall()

        # transforma para um formato fácil de usar no front
        data = [{"date": str(r["date"]), "total": r["total"]} for r in results]
        return {"ocorrencias_por_dia": data}

    except Exception as e:
        return {"error": str(e)}
    finally:
        cur.close()
        conn.close()
