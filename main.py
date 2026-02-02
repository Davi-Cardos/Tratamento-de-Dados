import os
from src.coletar import baixar
from src.transformar import processar

root = os.getcwd()
raw_path = os.path.join(root, 'dados_brutos')

print("--- Rodando ETL ---")

# Etapa 1
baixar(raw_path)

# Etapa 2
processar(raw_path)

print("--- Fim ---")