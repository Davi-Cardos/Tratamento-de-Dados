import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def baixar(pasta):
    base_url = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"
    anos_alvo = ["2024", "2023"] 
    
    os.makedirs(pasta, exist_ok=True)
    print(f"Início da varredura em: {base_url}")

    for ano in anos_alvo:
        url_ano = f"{base_url}{ano}/"
        print(f"\n Analisando diretório do ano: {url_ano}")
        
        try:
            response = requests.get(url_ano)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            
            links = soup.find_all('a')
            arquivos_zip = [
                link.get('href') for link in links 
                if link.get('href', '').lower().endswith('.zip')
            ]
            
            if not arquivos_zip:
                print(f" Nenhum ZIP encontrado em {ano} (Pode estar vazio).")
                continue

            print(f" Encontrados {len(arquivos_zip)} arquivos. Baixando...")

            for arquivo in arquivos_zip:
                url_download = urljoin(url_ano, arquivo)
                nome_arquivo = os.path.basename(arquivo)
                caminho_final = os.path.join(pasta, nome_arquivo)

                if os.path.exists(caminho_final):
                    print(f"   ✅ [Já existe] {nome_arquivo}")
                    continue

                print(f" Baixando: {nome_arquivo}...")
                
                with requests.get(url_download, stream=True) as r:
                    r.raise_for_status()
                    with open(caminho_final, "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                print(" Sucesso!")

        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 404:
                print(f" Pasta do ano {ano} não existe no servidor.")
            else:
                print(f" Erro de conexão em {ano}: {err}")
        except Exception as e:
            print(f" Erro inesperado: {e}")
