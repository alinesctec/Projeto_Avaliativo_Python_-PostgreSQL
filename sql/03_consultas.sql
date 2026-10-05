-- FASE 2 - CONSULTAS SQL E EXPORTAÇÃO PARA CSV


-- Primeiras 10 linhas da tabela
SELECT *
FROM raw_vendas
LIMIT 10;

-- Quantidade total de vendas
SELECT COUNT(*) AS total_vendas
FROM raw_vendas;

-- Filiais e cidades existentes
SELECT DISTINCT branch, city
FROM raw_vendas
ORDER BY branch;

-- Faturamento e quantidade de vendas por filial
SELECT
    branch                              AS filial,
    COUNT(*)                            AS qtd_vendas,
    ROUND(SUM(sales::NUMERIC), 2)       AS faturamento,
    ROUND(AVG(sales::NUMERIC), 2)       AS ticket_medio
FROM raw_vendas
GROUP BY branch
ORDER BY faturamento DESC;

-- Faturamento e avaliação média por linha de produto

SELECT
    product_line                        AS linha_produto,
    COUNT(*)                            AS qtd_vendas,
    ROUND(SUM(sales::NUMERIC), 2)       AS faturamento,
    ROUND(AVG(rating::NUMERIC), 2)      AS avaliacao_media
FROM raw_vendas
GROUP BY product_line
ORDER BY faturamento DESC;

-- Forma de pagamento mais usada

SELECT
    payment                             AS forma_pagamento,
    COUNT(*)                            AS qtd_vendas
FROM raw_vendas
GROUP BY payment
ORDER BY qtd_vendas DESC;

-- Valor médio, menor e maior venda

SELECT
    ROUND(AVG(sales::NUMERIC), 2)       AS valor_medio,
    ROUND(MIN(sales::NUMERIC), 2)       AS menor_venda,
    ROUND(MAX(sales::NUMERIC), 2)       AS maior_venda
FROM raw_vendas;

-- Filtro com WHERE: vendas acima de 1000

SELECT invoice_id, branch, product_line, sales
FROM raw_vendas
WHERE sales::NUMERIC > 1000
ORDER BY sales::NUMERIC DESC;

-- Vendas por dia da semana
-- -----------------------------------------------------------
-- A data está no formato mês/dia/ano (ex: 1/5/2019 = 5 de janeiro)
SELECT
    EXTRACT(ISODOW FROM TO_DATE(date, 'MM/DD/YYYY')) AS num_dia,
    TO_CHAR(TO_DATE(date, 'MM/DD/YYYY'), 'Day')      AS dia_semana,
    COUNT(*)                                         AS qtd_vendas
FROM raw_vendas
GROUP BY num_dia, dia_semana
ORDER BY qtd_vendas DESC;


-- 8. Filiais com faturamento acima de 100 mil (HAVING)

SELECT
    branch                              AS filial,
    ROUND(SUM(sales::NUMERIC), 2)       AS faturamento
FROM raw_vendas
GROUP BY branch
HAVING SUM(sales::NUMERIC) > 100000;


-- EXPORTAÇÃO PARA CSV (pasta data/raw/)


-- Base completa da camada Raw (entrada do Python)
\copy (SELECT invoice_id, branch, city, customer_type, gender, product_line, unit_price, quantity, tax_5_percent, sales, date, time, payment, cogs, gross_margin_percentage, gross_income, rating FROM raw_vendas ORDER BY invoice_id) TO 'data/raw/vendas_exportadas.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')

-- Resumo por filial
\copy (SELECT branch AS filial, city AS cidade, COUNT(*) AS qtd_vendas, ROUND(SUM(sales::NUMERIC), 2) AS faturamento FROM raw_vendas GROUP BY branch, city ORDER BY faturamento DESC) TO 'data/raw/resumo_filiais.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')
