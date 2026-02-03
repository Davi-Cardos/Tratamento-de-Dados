-- DDL Criação das tabelas
-- Optei por Postgres (SERIAL) 

DROP TABLE IF EXISTS despesas;
DROP TABLE IF EXISTS operadoras;

CREATE TABLE operadoras (
    reg_ans VARCHAR(10) PRIMARY KEY,
    cnpj VARCHAR(20),
    razao_social VARCHAR(255),
    modalidade VARCHAR(100),
    uf CHAR(2)
);

-- Index pra ajudar no filtro de UF
CREATE INDEX idx_operadora_uf ON operadoras(uf);

CREATE TABLE despesas (
    id SERIAL PRIMARY KEY, 
    reg_ans VARCHAR(10),
    data_lancamento DATE,
    trimestre INT,
    ano INT,
    vl_despesa DECIMAL(15,2), -- Decimal pra não dar erro de arredondamento
    descricao TEXT,
    CONSTRAINT fk_operadora FOREIGN KEY (reg_ans) REFERENCES operadoras(reg_ans)
);

CREATE INDEX idx_despesa_periodo ON despesas(ano, trimestre);