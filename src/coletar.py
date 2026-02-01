import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def baixar(pasta):
    base_url = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"
    periodos = [("2024", "03"), ("2024", "02"), ("2024", "01")]
    os.makedirs(pasta, exist_ok=True)
    print (f" Iniciando downloads para: {pasta}")

    for ano, trimestre in periodos:
        url_arquivo = f"{base_url}{ano}/{trimestre}/"

        print(f"\n Acessando diretório: {url_arquivo}")

        response = requests.get(url_arquivo)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        arquivos_zip = [link.get('href') for link in links if link.get('href', '').endswith('zip')]
        
        if not arquivos_zip:
            print (f"Nenhum arquivo .zip achado em {ano}/{trimestre}")
            continue

        for arquivo in arquivos_zip:
            url_download = urljoin(url_arquivo, arquivo)
            nome_arquivo = os.path.basename(arquivo)
            caminho_final = os.path.join(pasta, nome_arquivo)

            if os.path.exists(caminho_final):
                print (f"Arquivo já existe (skip): {nome_arquivo}")
                continue

            print (f"Baixando: {nome_arquivo}...")

            with requests.get(url_download, stream=True) as r:
                r.raise_for_status()
                with open (caminho_final, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            print(f"Sucesso!")
