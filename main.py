import os
from src.coletar import baixar
from src.transformar import processar
from src.limpeza import limpar_dados
from src.validando import enriquecer_dados

root = os.getcwd()
raw_path = os.path.join(root, 'dados_brutos')

print("--- Rodando ETL ---")

# Etapa 1
baixar(raw_path)

# Etapa 2
processar(raw_path)
limpar_dados()
enriquecer_dados()

print("--- Fim ---")