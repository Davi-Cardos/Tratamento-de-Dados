--Query 1: Top 5 crescimento

WITH inicio AS (
    SELECT reg_ans, SUM(vl_despesa) as total_ini
    FROM despesas WHERE ano = 2023 AND trimestre = 1
    GROUP BY reg_ans
),
fim AS (
    SELECT reg_ans, SUM(vl_despesa) as total_fim
    FROM despesas WHERE ano = 2023 AND trimestre = 4
    GROUP BY reg_ans
)
SELECT 
    op.razao_social,
    inicio.total_ini,
    fim.total_fim,
    ((fim.total_fim - inicio.total_ini) / inicio.total_ini) * 100 as crescimento_pct
FROM inicio
JOIN fim ON inicio.reg_ans = fim.reg_ans
JOIN operadoras op ON inicio.reg_ans = op.reg_ans
ORDER BY crescimento_pct DESC
LIMIT 5;


-- Query 2: Total e Média por UF
SELECT 
    op.uf,
    SUM(d.vl_despesa) as total,
    AVG(d.vl_despesa) as media_lancamento
FROM operadoras op
JOIN despesas d ON op.reg_ans = d.reg_ans
GROUP BY op.uf
ORDER BY total DESC
LIMIT 5;


-- Query 3: Operadoras acima da média em pelo menos 2 trimestres
-- Calcular a media do trimestre e comparar na bruta

SELECT 
    op.razao_social,
    COUNT(*) as qtd_trimestres_acima
FROM despesas d
JOIN operadoras op ON d.reg_ans = op.reg_ans
JOIN (
    SELECT ano, trimestre, AVG(vl_despesa) as media_mercado
    FROM despesas 
    GROUP BY ano, trimestre
) m ON d.ano = m.ano AND d.trimestre = m.trimestre
WHERE d.vl_despesa > m.media_mercado
GROUP BY op.razao_social
HAVING COUNT(*) >= 2; 