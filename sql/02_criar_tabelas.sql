
-- FASE 0 - CRIAÇÃO DAS TABELAS (RAW E TRATADA)

-- 1. CAMADA RAW (dados brutos)

DROP TABLE IF EXISTS raw_vendas;

CREATE TABLE raw_vendas (
    invoice_id              TEXT PRIMARY KEY,
    branch                  TEXT,
    city                    TEXT,
    customer_type           TEXT,
    gender                  TEXT,
    product_line            TEXT,
    unit_price              TEXT,
    quantity                TEXT,
    tax_5_percent           TEXT,
    sales                   TEXT,
    date                    TEXT,
    time                    TEXT,
    payment                 TEXT,
    cogs                    TEXT,
    gross_margin_percentage TEXT,
    gross_income            TEXT,
    rating                  TEXT,
    arquivo_origem          TEXT DEFAULT 'SuperMarketAnalysis.csv',
    data_carga              TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. CAMADA TRATADA (dados limpos)

DROP TABLE IF EXISTS vendas_tratadas;

CREATE TABLE vendas_tratadas (
    id_venda          VARCHAR(50)   NOT NULL,
    filial            VARCHAR(10)   NOT NULL,
    cidade            VARCHAR(100)  NOT NULL,
    tipo_cliente      VARCHAR(50),
    genero            VARCHAR(20),
    linha_produto     VARCHAR(150)  NOT NULL,
    preco_unitario    NUMERIC(10,2) NOT NULL,
    quantidade        INTEGER       NOT NULL,
    imposto           NUMERIC(10,2) NOT NULL,
    valor_total       NUMERIC(12,2) NOT NULL,
    data_venda        DATE          NOT NULL,
    hora_venda        TIME          NOT NULL,
    forma_pagamento   VARCHAR(50)   NOT NULL,
    custo_mercadoria  NUMERIC(12,2) NOT NULL,
    margem_percentual NUMERIC(10,2),
    receita_bruta     NUMERIC(12,2) NOT NULL,
    avaliacao         NUMERIC(4,2)  NOT NULL,

    
    CONSTRAINT pk_vendas_tratadas PRIMARY KEY (id_venda),
    CONSTRAINT ck_preco_unitario    CHECK (preco_unitario >= 0),
    CONSTRAINT ck_quantidade        CHECK (quantidade > 0),
    CONSTRAINT ck_imposto           CHECK (imposto >= 0),
    CONSTRAINT ck_valor_total       CHECK (valor_total >= 0),
    CONSTRAINT ck_custo_mercadoria  CHECK (custo_mercadoria >= 0),
    CONSTRAINT ck_receita_bruta     CHECK (receita_bruta >= 0),
    CONSTRAINT ck_avaliacao         CHECK (avaliacao BETWEEN 0 AND 10),
    CONSTRAINT ck_forma_pagamento   CHECK (
        forma_pagamento IN ('Cash', 'Credit card', 'Ewallet')
    )
);
