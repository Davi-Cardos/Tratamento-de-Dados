import pandas as pd
import requests
import os
from bs4 import BeautifulSoup

def enriquecer_dados():
    print("--- Iniciando Validação ---")
    
    url_base = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/"
    csv_cadastro = "cadastros_ans.csv"
    
    if not os.path.exists(csv_cadastro):
        print(" Baixando tabela de operadoras  ")
        try:
            r = requests.get(url_base)
            soup = BeautifulSoup(r.text, 'html.parser')
            link = [a['href'] for a in soup.find_all('a') if a['href'].lower().endswith('.csv')][0]
            
            full_link = url_base + link
            with requests.get(full_link, stream=True) as req:
                with open(csv_cadastro, 'wb') as f:
                    [f.write(c) for c in req.iter_content(8192)]
        except Exception as e:
            print(f" Erro ao baixar cadastro: {e}")
            return
        
    df_despesas = pd.read_csv("despesas_limpas.csv", sep=';', encoding='utf-8', dtype=str)
    df_cadastro = pd.read_csv(csv_cadastro, sep=';', encoding='latin-1', dtype=str, on_bad_lines='skip')
    df_cadastro.rename(columns={'REGISTRO_OPERADORA': 'REG_ANS'}, inplace=True)
    
    cols_quero = ['REG_ANS', 'CNPJ', 'Razao_Social', 'Modalidade', 'UF']
    cols_existentes = [c for c in cols_quero if c in df_cadastro.columns]
    df_cadastro = df_cadastro[cols_existentes]

    print(" Cruzando tabelas  ")
    df_final = pd.merge(df_despesas, df_cadastro, on='REG_ANS', how='left')
    df_final['CNPJ'] = df_final['CNPJ'].fillna("NÃO ENCONTRADO")
    
    saída = "resultado_final_teste.csv"
    df_final.to_csv(saída, index=False, sep=';', encoding='utf-8')
    
    print(f" CONCLUÍDO: {saída}")
    print(f"  Total de linhas: {len(df_final)}")
    print(f"  Operadoras sem cadastro: {df_final['Razao_Social'].isna().sum()}")

if __name__ == "__main__":
    enriquecer_dados()