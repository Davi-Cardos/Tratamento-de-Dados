import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import math

app = FastAPI(title="API Intuitive Care")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CARREGAMENTO DOS DADOS ---
try:
    print("Tentando carregar CSV...")
    # Tentando ler com UTF-8 e ponto e vírgula
    df = pd.read_csv("despesas_agregadas.csv", sep=';', encoding='utf-8')
    
    # Limpeza no CNPJ
    if 'CNPJ' in df.columns:
        df['CNPJ'] = df['CNPJ'].astype(str).str.replace(r'\.0$', '', regex=True)
    
    print(f"Sucesso! {len(df)} registros carregados.")
except Exception as e:
    print(f"Erro ao ler CSV: {e}")
    df = pd.DataFrame()

# --- ROTAS ---

@app.get("/api/operadoras")
def listar_operadoras(
    page: int = Query(1, gt=0), 
    limit: int = Query(10, gt=0), 
    search: Optional[str] = None
):
    if df.empty:
        return {"data": [], "meta": {"total": 0}}

    data_filtered = df.copy()

    # Buscando
    if search:
        search_term = search.lower()
        # Procura em Razao_Social e UF
        mask = (
            data_filtered['Razao_Social'].fillna('').astype(str).str.lower().str.contains(search_term) |
            data_filtered['UF'].fillna('').astype(str).str.lower().str.contains(search_term)
        )
        data_filtered = data_filtered[mask]

    # Paginação
    total_items = len(data_filtered)
    start = (page - 1) * limit
    end = start + limit
    
    # JSON: substitui NaN por None e infinitos
    paginated_data = data_filtered.iloc[start:end].where(pd.notnull(data_filtered), None).to_dict(orient="records")

    return {
        "data": paginated_data,
        "meta": {
            "page": page,
            "limit": limit,
            "total_items": total_items,
            "total_pages": math.ceil(total_items / limit)
        }
    }
@app.get("/api/estatisticas")
def obter_estatisticas():
    """
    Retorna métricas consolidadas.
    """
    if df.empty:
        return {"total_despesas": 0, "media_por_operadora": 0, "top_5": []}
    
    col_valor = 'Total_Despesas' 
    if col_valor not in df.columns:
        # Tentando achar outra coluna numérica se o nome mudar
        cols_num = df.select_dtypes(include=['float', 'int']).columns
        if len(cols_num) > 0:
            col_valor = cols_num[-1]
        else:
            return {"erro": "Coluna de valor não encontrada"}
    
    # Cálculos seguros 
    total_geral = df[col_valor].fillna(0).sum()
    media_geral = df[col_valor].fillna(0).mean()
    
    # Top 5
    top_5 = df.nlargest(5, col_valor)[['Razao_Social', col_valor]].fillna(0).to_dict(orient="records")
    
    return {
        "total_despesas": float(total_geral),
        "media_por_operadora": float(media_geral),
        "top_5_operadoras": top_5 
    }

@app.get("/")
def health_check():
    return {"status": "online"}