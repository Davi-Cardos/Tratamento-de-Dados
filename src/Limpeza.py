import pandas as pd
import os

def limpar_dados():
    input_file = "consolidado_despesas.csv"
    output_file = "despesas_limpas.csv"
    
    print(f"--- Iniciando Limpeza de {input_file} ---")
    
    if not os.path.exists(input_file):
        print("❌ Arquivo consolidado não encontrado!")
        return
    
    chunk_size = 100000
    chunks = []
    contador = 0

    reader = pd.read_csv(input_file, sep=';', encoding='utf-8', chunksize=chunk_size, dtype=str)

    for df in reader:
        contador += 1
        print(f"   Processando lote {contador}...", end='\r')

        # Na ANS, Grupo 4 = Despesas Assistenciais
        mask_despesa = df['CD_CONTA_CONTABIL'].str.startswith('4', na=False)
        
        mask_texto = df['DESCRICAO'].str.contains('EVENTO|SINISTRO|INDENIZ', case=False, na=False)
        
        df_filtrado = df[mask_despesa & mask_texto].copy()

        if df_filtrado.empty:
            continue

        def limpar_valor(val):
            try:
                if isinstance(val, str):
                    val = val.replace('.', '').replace(',', '.')
                return float(val)
            except:
                return 0.0

        df_filtrado['VL_SALDO_FINAL'] = df_filtrado['VL_SALDO_FINAL'].apply(limpar_valor)

        df_filtrado = df_filtrado[df_filtrado['VL_SALDO_FINAL'] > 0]
       
        df_filtrado = df_filtrado[[
            'REG_ANS', 'DESCRICAO', 'DATA', 'VL_SALDO_FINAL', 'TRIMESTRE', 'ANO'
        ]]
        
        chunks.append(df_filtrado)

    print(f"\n  Juntando os pedaços...")
    
    if chunks:
        df_final = pd.concat(chunks, ignore_index=True)
        
        # Salvando
        df_final.to_csv(output_file, index=False, sep=';', encoding='utf-8')
        print(f" LIMPEZA CONCLUÍDA: {output_file}")
        print(f"  Linhas originais: +6 Milhões")
        print(f"  Linhas finais (Despesas): {len(df_final)}")
        print("  Nota: Mantivemos REG_ANS. O CNPJ virá no próximo passo (Join).")
    else:
        print(" Nenhuma linha de despesa encontrada. Verifique o filtro.")

if __name__ == "__main__":
    limpar_dados()