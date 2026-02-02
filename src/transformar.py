import os
import zipfile
import pandas as pd
from glob import glob

def processar(path_raw):
    arquivos = glob(os.path.join(path_raw, "*.zip"))
    lista_dfs = []

    print(f"Encontrado {len(arquivos)} arquivos ZIP.")

    for f in arquivos:
        print(f"\n--- Abrindo: {os.path.basename(f)} ---")
        try:
            name = os.path.basename(f).replace('.zip', '')
            parts = name.upper().split('T')
            
            if len(parts) < 2:
                print(f" Nome fora do padrão: {name}")
                continue
                
            tri, ano = parts[0], parts[1]
            
            with zipfile.ZipFile(f, 'r') as z:
                csvs = [x for x in z.namelist() if x.lower().endswith('.csv')]
                
                if not csvs:
                    print(" Nenhum CSV no ZIP.")
                    continue
                
                csv_target = csvs[0]
                print(f" Lendo CSV: {csv_target}")

                with z.open(csv_target) as data:
                    df = pd.read_csv(data, sep=';', encoding='latin-1', on_bad_lines='skip')
                    
                df['TRIMESTRE'] = tri
                df['ANO'] = ano
                lista_dfs.append(df)
                print(f" Sucesso! {len(df)} linhas.")
                
        except Exception as e:
            print(f" ERRO no arquivo {f}: {e}")

    if lista_dfs:
        full_df = pd.concat(lista_dfs, ignore_index=True)
        full_df.to_csv("consolidado_despesas.csv", sep=';', index=False, encoding='utf-8')
        print(f"\n SUCESSO! Arquivo 'consolidado_despesas.csv' gerado com {len(full_df)} linhas.")
    else:
        print("\n Nenhum dado processado.")