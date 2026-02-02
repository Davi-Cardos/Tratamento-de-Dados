import pandas as pd
import os

def espiar_cadastro():
    arquivo = "cadastros_ans.csv"

    print(f"--- Espiando colunas de {arquivo} ---")
    
    try:
        df = pd.read_csv(arquivo, sep=';', encoding='latin-1', nrows=5)
        print("\n📋 COLUNAS ENCONTRADAS:")
        for col in df.columns:
            print(f"   '{col}'")
    except Exception as e:
        print(f"Erro ao ler: {e}")

if __name__ == "__main__":
    espiar_cadastro()