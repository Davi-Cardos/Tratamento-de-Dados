from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import math

app = FastAPI()
# Configuração do CORS para o Vue.js conseguir acessar
# Justificativa: Permite que o frontend rode em porta diferente do backend (localhost:8000 vs localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Variável global para manter os dados em memória
df_despesas = pd.DataFrame()

# Escolha técnica: Carregar o CSV na memória ao iniciar a API.
# sem precisar de um banco de dados complexo rodando localmente.
try:
    print("Carregando dados do CSV...")
    # Troque a linha do pd.read_csv por esta:
    df_despesas = pd.read_csv("despesas_agregadas.csv", sep=';', encoding='latin1')
    
    # Tratamento de dados: O Pandas as vezes lê CNPJ como número, então converti para string e removi o '.0' que aparece.
    if 'CNPJ' in df_despesas.columns:
        df_despesas['CNPJ'] = df_despesas['CNPJ'].astype(str).str.replace('.0', '', regex=False)
    print(f"Dados carregados com sucesso! Total de registros: {len(df_despesas)}")

except Exception as e:
    print(f"Erro ao ler o arquivo CSV: {e}")
    # Cria um dataframe vazio para a API não cair
    df_despesas = pd.DataFrame()

@app.get("/")
def home():
    return {"message": "API de Despesas da ANS Online"}

@app.get("/api/operadoras")
def listar_operadoras(page: int = 1, limit: int = 10, search: str = ""):
    """
    Retorna lista de operadoras paginada.
    Trade-off: Utilizei paginação baseada em offset (page/limit) pois é mais simples de implementar
    e funciona bem para dados que não mudam em tempo real (estáticos no CSV).
    """
    if df_despesas.empty:
        return {"data": [], "meta": {"total": 0}}

    # Filtragem
    df_filtrado = df_despesas.copy()
    if search:
        termo = search.lower()
        # Busca tanto no nome quanto na UF
        df_filtrado = df_filtrado[
            df_filtrado['RazaoSocial'].astype(str).str.lower().str.contains(termo) | 
            df_filtrado['UF'].astype(str).str.lower().str.contains(termo)
        ]

    # Paginação manual
    total_registros = len(df_filtrado)
    total_paginas = math.ceil(total_registros / limit)
    
    inicio = (page - 1) * limit
    fim = inicio + limit
    
    # Slice do dataframe para pegar apenas a página atual
    resultado = df_filtrado.iloc[inicio:fim].to_dict(orient="records")
    return {
        "data": resultado,
        "meta": {
            "page": page,
            "limit": limit,
            "total": total_registros,
            "total_pages": total_paginas
        }
    }

@app.get("/api/operadoras/{cnpj}")
def buscar_operadora(cnpj: str):
    """
    Busca detalhes de uma operadora específica pelo CNPJ.
    """
    if df_despesas.empty:
        raise HTTPException(status_code=500, detail="Base de dados não carregada")

    # Filtra pelo CNPJ exato
    operadora = df_despesas[df_despesas['CNPJ'] == cnpj]

    if operadora.empty:
        raise HTTPException(status_code=404, detail="Operadora não encontrada")

    # Retorna o primeiro registro que encontrar
    return operadora.iloc[0].to_dict()

@app.get("/api/estatisticas")
def estatisticas():
    """
    Retorna dados agregados para o dashboard.
    Trade-off: Calculando em tempo real.
    Justificativa: Como a leitura é em memória com a biblioteca Pandas, a operação é rápida o suficiente para o volume atual.
    """
    if df_despesas.empty:
        return {"erro": "Sem dados disponíveis"}
    
    coluna_valor = 'Valor_Total_Despesas' 
    # Só prevenção caso o nome da coluna seja diferente
    if coluna_valor not in df_despesas.columns:
        # Tentando pegar a última coluna numérica se não achar pelo nome
        coluna_valor = df_despesas.select_dtypes(include=['float', 'int']).columns[-1]

    total_geral = df_despesas[coluna_valor].sum()
    media_geral = df_despesas[coluna_valor].mean()
    
    # Pega as top 5
    top_5 = df_despesas.nlargest(5, coluna_valor)[['RazaoSocial', 'UF', coluna_valor]].to_dict(orient="records")

    return {
        "total_despesas": total_geral,
        "media_por_operadora": media_geral,
        "top_5": top_5
    }