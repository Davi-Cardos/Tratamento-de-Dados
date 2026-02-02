import pandas as pd
import os

def agregar_dados():
    print("--- Iniciando Agregação Estatística (Teste 2.3) ---")
    
    arquivo_entrada = "resultado_final_teste.csv"
    arquivo_saida = "despesas_agregadas.csv"

    df = pd.read_csv(arquivo_entrada, sep=';', encoding='utf-8')

    df['VL_SALDO_FINAL'] = pd.to_numeric(df['VL_SALDO_FINAL'], errors='coerce').fillna(0)
    # Agrupamento
    print("  Calculando estatísticas (Soma, Média, Desvio Padrão)...")
    grupo = df.groupby(['Razao_Social', 'UF'])['VL_SALDO_FINAL']
    
    # Aplica as funções matemáticas
    df_agregado = grupo.agg(
        Total_Despesas='sum',
        Media_Trimestral='mean',
        Desvio_Padrao='std',
        Contagem='count' 
    ).reset_index()

    df_agregado['Desvio_Padrao'] = df_agregado['Desvio_Padrao'].fillna(0)
    
    # Ordenando por maior despesa para facilitar a análise visual
    df_agregado = df_agregado.sort_values(by='Total_Despesas', ascending=False)
    df_agregado.to_csv(arquivo_saida, index=False, sep=';', encoding='utf-8')
    print(f" SUCESSO! Arquivo gerado: {arquivo_saida}")
    print(f" Maior Despesa: {df_agregado.iloc[0]['Razao_Social']} ({df_agregado.iloc[0]['UF']})")

if __name__ == "__main__":
    agregar_dados()