Primeiro Commit: Iniciei o repositório no Github

Segundo Commit: Etapa de Coletar Dados sendo feita. Me deparei com o desafio inicial de buscar os arquivos com os nomes certos, pensei primeiro em tentar adivinhar o nome do arquivo padrão (ex: construir a string da URL baseada na data), porém se a ANS mudar uma letra no nome do arquivo, o script quebra e não encontra. Com isso busquei uma biblioteca para tornar dinâmico essa parte sendo resiliente a mudanças no nome do arquivo e usei a BeautifulSoup. Aonde o script acessa o diretório do servidor, baixa o HTML, faz o *parse* da página e lista todos os links disponíveis, filtrando apenas os que terminam em `.zip`.

    * *Prós:* **Alta Resiliência**. O script funciona independentemente do nome do arquivo, desde que ele seja um `.zip` dentro da pasta correta.
    * *Contras:* Adiciona uma dependência ao projeto (`beautifulsoup4`) e requer uma requisição HTTP extra para ler o diretório.

Também coloquei a extração em um arquivo denominado "coletar.py" separado na pasta "src" e fiz sua chamada de função no arquivo main, para ficar melhor organizado.