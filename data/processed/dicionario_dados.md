# Dicionário de Dados – vendas_tratadas.csv

**Arquivo:** `data/processed/vendas_tratadas.csv`
**Gerado por:** `src/02_etl_vendas.py`
**Origem:** `data/raw/vendas_exportadas.csv` (exportado da tabela `raw_vendas`)
**Registros:** 1000 vendas, de 01/01/2019 a 30/03/2019
**Separador:** vírgula | **Codificação:** UTF-8

## 1. Colunas principais (iguais à tabela `vendas_tratadas` do banco)

| Coluna | Tipo | Restrição | Coluna original | Descrição |
|---|---|---|---|---|
| id_venda | VARCHAR(50) | PRIMARY KEY, NOT NULL | Invoice ID | Código único da venda |
| filial | VARCHAR(10) | NOT NULL | Branch | Filial (Alex, Cairo, Giza) |
| cidade | VARCHAR(100) | NOT NULL | City | Cidade da filial |
| tipo_cliente | VARCHAR(50) | — | Customer type | Member (membro) ou Normal |
| genero | VARCHAR(20) | — | Gender | Gênero do cliente |
| linha_produto | VARCHAR(150) | NOT NULL | Product line | Categoria do produto |
| preco_unitario | NUMERIC(10,2) | CHECK >= 0 | Unit price | Preço de uma unidade |
| quantidade | INTEGER | CHECK > 0 | Quantity | Unidades compradas |
| imposto | NUMERIC(10,2) | CHECK >= 0 | Tax 5% | Imposto de 5% sobre a venda |
| valor_total | NUMERIC(12,2) | CHECK >= 0 | Sales | Valor final (preço × quantidade + imposto), conferido no ETL |
| data_venda | DATE | NOT NULL | Date | Data da venda, convertida de M/D/AAAA para AAAA-MM-DD |
| hora_venda | TIME | NOT NULL | Time | Hora da venda, convertida de 12h (AM/PM) para 24h |
| forma_pagamento | VARCHAR(50) | NOT NULL | Payment | Cash, Credit card ou Ewallet |
| custo_mercadoria | NUMERIC(12,2) | CHECK >= 0 | cogs | Custo dos produtos vendidos |
| margem_percentual | NUMERIC(10,2) | — | gross margin percentage | Margem bruta em % (4,76 em todas as linhas) |
| receita_bruta | NUMERIC(12,2) | CHECK >= 0 | gross income | Lucro bruto da venda |
| avaliacao | NUMERIC(4,2) | CHECK entre 0 e 10 | Rating | Nota dada pelo cliente |

## 2. Colunas derivadas (criadas no Pandas, só no CSV)

| Coluna | Tipo | Como foi criada |
|---|---|---|
| ano | INTEGER | Ano da `data_venda` |
| mes | INTEGER | Número do mês da `data_venda` (1 a 3) |
| nome_mes | TEXTO | Nome do mês em português |
| dia_semana | TEXTO | Dia da semana em português (Segunda a Domingo) |
| hora | INTEGER | Hora cheia da `hora_venda` (10 a 20) |
| periodo_dia | TEXTO | Manhã (até 11h59), Tarde (12h a 17h59), Noite (18h em diante) |
| faixa_valor | TEXTO | Até 100, 100 a 300, 300 a 600, Acima de 600 |
| classificacao_avaliacao | TEXTO | Baixa (até 6), Média (6 a 8), Alta (8 a 10) |

## 3. Tratamentos aplicados

1. Colunas renomeadas de inglês para português (snake_case).
2. Espaços extras removidos dos textos.
3. Conversão de tipos: números, data e hora.
4. Verificação de nulos: nenhum encontrado (0 linhas removidas).
5. Verificação de duplicados: nenhum encontrado (0 linhas removidas).
6. Validação das regras do CHECK: todas as 1000 linhas aprovadas.
7. Conferência do `valor_total`: todas as linhas batem com o cálculo.
8. Valores numéricos arredondados para 2 casas decimais.
