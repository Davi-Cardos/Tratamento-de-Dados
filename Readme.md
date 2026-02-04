# Teste Técnico de Tratamento de Dados

Autor: Davi Cardoso de Oliveira

Este projeto é uma solução Full Stack para o desafio técnico da Intuitive Care, abrangendo desde a coleta e transformação de dados da ANS até a exposição em uma API e visualização em Dashboard interativo.

## Como Executar o Projeto

### Pré-requisitos
* Python 3.8+
* Navegador Web (Chrome/Edge/Firefox)

### Instalação das Dependências
No terminal, na raiz do projeto, execute:
```bash
pip install pandas sqlalchemy fastapi uvicorn pymysql
```
### Coletando e Transformando os arquivos ANS
No terminal execute:
```bash
py main.py
```
### 1. Executando a API (Backend)
Usei o FastAPI porque é rápido e já cria a documentação sozinho. No terminal, rode:
```bash
uvicorn api:app --reload
```
Aguarde a mensagem: *Application startup complete.*

### 2. Acessando o Dashboard (Frontend)
Não é necessário instalação de Node.js ou build complexo.

1º passo: Vá até a pasta do projeto.

2º passo: Dê um duplo clique no arquivo index.html.

3° passo: O painel abrirá no seu navegador, conectando-se automaticamente à API local.

## Relatórios dos Commits feitos conforme ia desenvolvendo o projeto

*Primeiro Commit:* 

Iniciei o repositório no Github

*Segundo Commit:* 

Etapa de Coletar Dados sendo feita. Me deparei com o desafio inicial de buscar os arquivos com os nomes certos, pensei primeiro em tentar adivinhar o nome do arquivo padrão (ex: construir a string da URL baseada na data), porém se a ANS mudar uma letra no nome do arquivo, o script quebra e não encontra. Com isso busquei uma biblioteca para tornar dinâmico essa parte sendo resiliente a mudanças no nome do arquivo e usei a BeautifulSoup. Aonde o script acessa o diretório do servidor, baixa o HTML, faz o *parse* da página e lista todos os links disponíveis, filtrando apenas os que terminam em `.zip`.

   **Prós:** **Alta Resiliência**. O script funciona independentemente do nome do arquivo, desde que ele seja um `.zip` dentro da pasta correta.
   **Contras:** Adiciona uma dependência ao projeto (`beautifulsoup4`) e requer uma requisição HTTP extra para ler o diretório.

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

*Décimo quinto commit:*

Busquei fazer aqui uma atualização na paginação, percebi que como tinha 90 páginas, se alguém quisesse ir para a última ia precisar clicar 90 vezes, e por isso coloquei 2 botões a mais na paginação, um que leva para o final e outro que leva para o início da paginação.

*Décimo sexto commit:*

Escrita do Readme finalizada incluindo os trade-offs e as instruções de como rodar o projeto.

## Detalhes das Etapas e Trade-offs Técnicos

### Etapa 1 e 2: Engenharia de Dados (ETL)
Estratégia de Processamento: Optei pelo uso da biblioteca Pandas processando os arquivos em memória.

Justificativa: Dado o volume de dados dos últimos 3 trimestres, o Pandas oferece a melhor relação entre velocidade de desenvolvimento e uma boa execução, sem precisar configurar um Spark ou ferramenta de Big Data para este escopo.

Tratamento de Inconsistências: Implementei normalização de encoding e limpeza de caracteres em campos numéricos/CNPJ para garantir a integridade das chaves de junção.

### Etapa 3: Banco de Dados e SQL
Modelagem: Os dados foram estruturados separando métricas financeiras e dados cadastrais, facilitando consultas analíticas.

Tipagem Monetária: Utilizei estritamente DECIMAL(15,2) ao invés de FLOAT.

Justificativa: Em sistemas financeiros, a precisão é muito importante. O tipo float pode introduzir erros de arredondamento em somatórios de grandes volumes.

### Etapa 4: API e Interface Web (Full Stack)
*4.1. Backend (FastAPI)*

Escolha do Framework: Optei por FastAPI ao invés de Flask.

Justificativa: O FastAPI é assíncrono nativamente, possui validação de dados automática e gera a documentação Swagger UI sem esforço extra, o que acelera o desenvolvimento e facilita a avaliação da API.

Paginação: Offset-based

Justificativa: Para interfaces de tabelas onde o usuário navega página a página, o método limit/offset é o mais intuitivo e simples de implementar. Cursor-based seria excessivo para dados que não são atualizados em tempo real.

Estatísticas: On-the-fly

Justificativa: Como os dados são carregados em memória na inicialização da API, os cálculos de agregação levam milissegundos. Implementar cache adicionaria complexidade de infraestrutura desnecessária para o volume atual.

*4.2. Frontend (Vue.js via CDN)*

Arquitetura "No-Build": O Frontend foi construído em um único arquivo HTML importando Vue 3 e Tailwind CSS via CDN.

Justificativa: Elimina a necessidade de configurar um ambiente Node.js complexo para avaliar o teste.

Busca: Server-Side

Justificativa: A filtragem é realizada no Backend. Se filtrássemos apenas no Frontend, a busca estaria limitada aos 10 itens da página atual em vez de todo o dataset.

## Arquivos do Projeto
**api.py**: O servidor Python.

**index.html**: O site.

**despesas_agregadas.csv**: O arquivo de dados que a API lê.

**main.py**: O código que tratou os dados.  Obs: Na pasta "src" estão os scripts das funções executadas no código "main.py"

**queries.sql** e **tabelas.sql**: A parte de banco de dados.
