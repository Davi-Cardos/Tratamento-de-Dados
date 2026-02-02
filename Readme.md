*Primeiro Commit:* 

Iniciei o repositório no Github

*Segundo Commit:* 

Etapa de Coletar Dados sendo feita. Me deparei com o desafio inicial de buscar os arquivos com os nomes certos, pensei primeiro em tentar adivinhar o nome do arquivo padrão (ex: construir a string da URL baseada na data), porém se a ANS mudar uma letra no nome do arquivo, o script quebra e não encontra. Com isso busquei uma biblioteca para tornar dinâmico essa parte sendo resiliente a mudanças no nome do arquivo e usei a BeautifulSoup. Aonde o script acessa o diretório do servidor, baixa o HTML, faz o *parse* da página e lista todos os links disponíveis, filtrando apenas os que terminam em `.zip`.

    * *Prós:* **Alta Resiliência**. O script funciona independentemente do nome do arquivo, desde que ele seja um `.zip` dentro da pasta correta.
    * *Contras:* Adiciona uma dependência ao projeto (`beautifulsoup4`) e requer uma requisição HTTP extra para ler o diretório.

Também coloquei a extração em um arquivo denominado "coletar.py" separado na pasta "src" e fiz sua chamada de função "baixar" no arquivo main, para ficar melhor organizado.

*Terceiro Commit:*

Após fazer o Try/Catch para lidar com erros de arquivos não encontrados e acabar não encontrando nenhum, verifiquei que estava com o pensamento errado de "períodos", utilizando tuplas a cada trimestre de um ano, porém o ANS não estava separando assim mas sim em anos, mudando as tuplas em períodos para anos "2024, 2023", consegui entrar nas pastas do arquivo do site com a função de "baixar" do arquivo "coletar.py" e baixar os arquivos zip da ANS.

*Quarto Commit:*

Etapa 2 iniciada com a análise dos arquivos, inicialmente utilizando a biblioteca pandas para me auxiliar na leitura dos arquivos, tive uma dificuldade inicial pois eles estavam com uma codificaçao mais antiga, mas após identifica-la, consegui ler todos os arquivos e gerar um novo arquivo com as despesas consolidadas.

*Quinto e Sexto Commit:*

Busquei fazer uma limpeza no arquivo enorme gerado e para isso primeiro criei um arquivo somente para espiar as primeiras 5 linhas de todas as colunas para saber como estavam os dados e com isso criei o arquivo limpeza.py, inicialmente estava travando pela quantidade de memória absurda necessária para ler o arquivo, então aceitei que não conseguiria conseguir CNPJ agora. Filtrei só as despesas usando o REG_ANS e no próximo commit cruzar com a tabela de cadastro para pegar o CNPJ e o Nome.

*Sétimo Commit:*

Primeiro vi os nomes das colunas todas dos cadatros com um código simples de print "espiar_cadastro.py", e então tendo essa informação fiz o arquivo "validando.py" onde fiz o cruzamento das informações como o CNPJ com os registros ANS, gerando um arquivo final de "resultado_final_teste.csv" com os resultados das validações e o número de linhas de operadoras sem cadastro que foi de 8.477 linhas, são operadoras que mandaram balanços contábeis em 2023/2024, mas não constam mais na lista de Ativas hoje.