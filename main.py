print(">>> O PYTHON ESTÁ LENDO O ARQUIVO! <<<")
import os
from src.coletar import baixar

def main():
    print(">>> Entrou na função main <<<")
    print(">>> Início do Teste Intuitive Care <<<")

    pasta_caminho = os.path.join(os.getcwd(), "dados_brutos")

    print("--- Etapa de Coleta de Dados ---")
    baixar(pasta_caminho)

    print("\n>>> Processo de download finalizado. Verifique a pasta 'dados_brutos'. ")
main()