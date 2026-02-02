import pandas as pd

def espiar():
    print("--- Analisando o Arquivo Grande (consolidado_despesas.csv) ---")
    
    df = pd.read_csv("consolidado_despesas.csv", sep=';', nrows=5, encoding='utf-8')
    
    print("\n AS COLUNAS SÃO:")
    for col in df.columns:
        print(f"   - {col}")
        
    print("\n PRIMEIRAS 5 LINHAS:")
    print(df.to_string())

if __name__ == "__main__":
    espiar()