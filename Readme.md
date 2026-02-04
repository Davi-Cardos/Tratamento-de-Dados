*Primeiro Commit:* 

Iniciei o repositório no Github

*Segundo Commit:* 

Etapa de Coletar Dados sendo feita. Me deparei com o desafio inicial de buscar os arquivos com os nomes certos, pensei primeiro em tentar adivinhar o nome do arquivo padrão (ex: construir a string da URL baseada na data), porém se a ANS mudar uma letra no nome do arquivo, o script quebra e não encontra. Com isso busquei uma biblioteca para tornar dinâmico essa parte sendo resiliente a mudanças no nome do arquivo e usei a BeautifulSoup. Aonde o script acessa o diretório do servidor, baixa o HTML, faz o *parse* da página e lista todos os links disponíveis, filtrando apenas os que terminam em `.zip`.

    * *Prós:* **Alta Resiliência**. O script funciona independentemente do nome do arquivo, desde que ele seja um `.zip` dentro da pasta correta.
    * *Contras:* Adiciona uma dependência ao projeto (`beautifulsoup4`) e requer uma requisição HTTP extra para ler o diretório.

Também coloquei a extração em um arquivo denominado "coletar.py" separado na pasta "src" e fiz sua chamada de função "baixar" no arquivo main, para ficar melhor organizado. 

Obs: Todos os outros novos arquivos das etapas 1 e 2 ficarão nessa pasta "src" com uma chamada de sua função pela main, somente para ficar melhor organizado.

*Terceiro Commit:*

Após fazer o Try/Catch para lidar com erros de arquivos não encontrados e acabar não encontrando nenhum, verifiquei que estava com o pensamento errado de "períodos", utilizando tuplas a cada trimestre de um ano, porém o ANS não estava separando assim mas sim em anos, mudando as tuplas em períodos para anos "2024, 2023", consegui entrar nas pastas do arquivo do site com a função de "baixar" do arquivo "coletar.py" e baixar os arquivos zip da ANS.

*Quarto Commit:*

Etapa 2 iniciada com a análise dos arquivos, inicialmente utilizando a biblioteca pandas para me auxiliar na leitura dos arquivos, tive uma dificuldade inicial pois eles estavam com uma codificaçao mais antiga, mas após identifica-la, consegui ler todos os arquivos e gerar um novo arquivo com as despesas consolidadas.

*Quinto e Sexto Commit:*

Busquei fazer uma limpeza no arquivo enorme gerado e para isso primeiro criei um arquivo somente para espiar as primeiras 5 linhas de todas as colunas para saber como estavam os dados e com isso criei o arquivo limpeza.py, inicialmente estava travando pela quantidade de memória absurda necessária para ler o arquivo, então aceitei que não conseguiria conseguir o CNPJ agora. Filtrei só as despesas usando o REG_ANS e no próximo commit cruzar com a tabela de cadastro para pegar o CNPJ e o Nome.

*Sétimo Commit:*

Primeiro vi os nomes das colunas todas dos cadatros com um código simples de print "espiar_cadastro.py", e então tendo essa informação fiz o arquivo "validando.py" onde fiz o cruzamento das informações como o CNPJ com os registros ANS, gerando um arquivo final de "resultado_final_teste.csv" com os resultados das validações e o número de linhas de operadoras sem cadastro, que foi de 8.477 linhas, são operadoras que mandaram balanços contábeis em 2023/2024, mas que não constam mais na lista de Ativas hoje.

*Oitavo Commit:* 

Etapa do teste de agregação estatística, aqui principalmente busquei a maior despesa após a validação, mas implementei também o desvio padrão, soma das despesas, média trimestral, contagem e ordenação das mesmas no final para obter a maior despesa do arquivo de resultado final.

*Nono e Décimo Commits:*

Apenas Removendo do histórico do Git os arquivos CSV e criando um gitignore para eles, pois alguns são muito grandes para eu poder lançar os commits no meu Github.

*Décimo primeiro commit:*

Criação de tabelas em SQL com o objetivo de estruturar os dados processados em um banco de dados relacional, a estrutura foi desenhada separando métricas quantitativas e atributos descritivos seguindo a lógica "Star Schema", facilitando a escrita de queries analíticas. Optei pelo uso de tipos `DECIMAL` para colunas monetárias ao invés de `FLOAT` ou `DOUBLE`. Isso elimina alguns erros de arredondamento em operações de ponto flutuante. 

Além da estruturação, desenvolvi queries SQL, incluindo:
1.  **Média dos Trimestres:** Cálculo agregado para identificar tendências macro.
2.  **Crescimento vs. Mercado:** Comparativo de performance para identificar empresas acima da média do setor.

*Décimo segundo commit:*

Backend iniciado, escrevendo a api para consumir os dados do CSV consolidado, coloquei alguns trade-offs escrito no código conforme ia fazendo, até o momento me deparei com um erro ao ler o arquivo mas o esqueleto da api está feito, próximo commit buscarei conseguir ler o arquivo.

*Décimo terceiro commit:*

Erro de ler o CSVs consertado, estava esquecendo de indicar os "sep" e o encoding mais antigo do CSV

*Décimo quarto commit:*

Frontend HTML com Vue.js finalizado, algumas alterações no backend "api" pois estava com dificuldade de ler algumas partes do CSV, troquei o "sep" para ponto e vírgula e o encoding deixei igual ao html UTF-8, assim consegui ler todas as informações e gerar os dados na tela do Vue.js, com um gráfico de donut para as 5 maiores despesas encontradas e um CSS básico para ficar visualmente bonito.