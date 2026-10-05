
import pandas as pd
from sqlalchemy import text

from config import CSV_EXPORTADO, CSV_TRATADO, PASTA_PROCESSED, criar_conexao

# Nomes novos das colunas (seguindo o dicionário de dados)
NOVOS_NOMES = {
    "invoice_id": "id_venda",
    "branch": "filial",
    "city": "cidade",
    "customer_type": "tipo_cliente",
    "gender": "genero",
    "product_line": "linha_produto",
    "unit_price": "preco_unitario",
    "quantity": "quantidade",
    "tax_5_percent": "imposto",
    "sales": "valor_total",
    "date": "data_venda",
    "time": "hora_venda",
    "payment": "forma_pagamento",
    "cogs": "custo_mercadoria",
    "gross_margin_percentage": "margem_percentual",
    "gross_income": "receita_bruta",
    "rating": "avaliacao",
}

COLUNAS_TEXTO = ["id_venda", "filial", "cidade", "tipo_cliente", "genero",
                 "linha_produto", "forma_pagamento"]

COLUNAS_NUMERICAS = ["preco_unitario", "imposto", "valor_total",
                     "custo_mercadoria", "margem_percentual",
                     "receita_bruta", "avaliacao"]

# Colunas que não podem ficar vazias (NOT NULL no banco)
COLUNAS_OBRIGATORIAS = ["id_venda", "filial", "cidade", "linha_produto",
                        "preco_unitario", "quantidade", "imposto",
                        "valor_total", "data_venda", "hora_venda",
                        "forma_pagamento", "custo_mercadoria",
                        "receita_bruta", "avaliacao"]

DIAS_SEMANA = {0: "Segunda", 1: "Terça", 2: "Quarta", 3: "Quinta",
               4: "Sexta", 5: "Sábado", 6: "Domingo"}

MESES = {1: "Janeiro", 2: "Fevereiro", 3: "Março"}


# Etapa 1: Ler os dados

def ler_dados():
    df = pd.read_csv(CSV_EXPORTADO, sep=",", dtype=str)
    print(f"Linhas lidas: {len(df)}")
    return df

# Etapa 2: Renomear colunas

def renomear_colunas(df):
    df = df.rename(columns=NOVOS_NOMES)
    print("Colunas renomeadas para português.")
    return df

# Etapa 3: Limpar os textos

def limpar_textos(df):
    for coluna in COLUNAS_TEXTO:
        df[coluna] = df[coluna].str.strip()
    print("Espaços extras removidos das colunas de texto.")
    return df


# Etapa 4: Converter os tipos (casting)

def converter_tipos(df):
    # errors="coerce" transforma valores inválidos em nulo (NaN),
    # assim eu consigo encontrar esses problemas na etapa seguinte
    for coluna in COLUNAS_NUMERICAS:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

    df["quantidade"] = pd.to_numeric(df["quantidade"], errors="coerce")
    df["quantidade"] = df["quantidade"].astype("Int64")

    # Data no formato mês/dia/ano -> 1/5/2019 vira 2019-01-05
    df["data_venda"] = pd.to_datetime(
        df["data_venda"], format="%m/%d/%Y", errors="coerce"
    )

    # Hora no formato 12h -> 1:08:00 PM vira 13:08:00
    df["hora_venda"] = pd.to_datetime(
        df["hora_venda"], format="%I:%M:%S %p", errors="coerce"
    ).dt.time

    print("Tipos convertidos (números, data e hora).")
    return df

# Etapa 5: Verificar e tratar valores nulos

def tratar_nulos(df):
    nulos = df.isnull().sum()
    print("Nulos por coluna depois da conversão:")
    print(nulos[nulos > 0] if nulos.sum() > 0 else "  Nenhum valor nulo.")

    # Campos opcionais: preencho com "Não informado"
    df["tipo_cliente"] = df["tipo_cliente"].fillna("Não informado")
    df["genero"] = df["genero"].fillna("Não informado")

    # Campos obrigatórios: se faltar, a linha não pode ser usada
    antes = len(df)
    df = df.dropna(subset=COLUNAS_OBRIGATORIAS)
    print(f"Linhas removidas por falta de dado obrigatório: {antes - len(df)}")
    return df

# Etapa 6: Remover duplicidades

def remover_duplicados(df):
    antes = len(df)
    df = df.drop_duplicates()
    df = df.drop_duplicates(subset="id_venda", keep="first")
    print(f"Linhas duplicadas removidas: {antes - len(df)}")
    return df

# Etapa 7: Validar regras de negócio (iguais aos CHECKs do banco)

def validar_regras(df):
    regras = (
        (df["preco_unitario"] >= 0)
        & (df["quantidade"] > 0)
        & (df["imposto"] >= 0)
        & (df["valor_total"] >= 0)
        & (df["custo_mercadoria"] >= 0)
        & (df["receita_bruta"] >= 0)
        & (df["avaliacao"].between(0, 10))
    )
    print(f"Linhas que não passaram nas regras: {(~regras).sum()}")
    df = df[regras].copy()

    # Conferência do valor total: preço x quantidade + imposto
    valor_calculado = df["preco_unitario"] * df["quantidade"] + df["imposto"]
    diferenca = (df["valor_total"] - valor_calculado).abs()
    print(f"Vendas com valor_total diferente do calculado: "
          f"{(diferenca > 0.01).sum()}")
    return df

# Etapa 8: Criar colunas derivadas

def criar_colunas_derivadas(df):
    df["ano"] = df["data_venda"].dt.year
    df["mes"] = df["data_venda"].dt.month
    df["nome_mes"] = df["mes"].map(MESES)
    df["dia_semana"] = df["data_venda"].dt.dayofweek.map(DIAS_SEMANA)

    # Hora como número (13:08 -> 13) para separar os períodos do dia
    df["hora"] = [h.hour for h in df["hora_venda"]]
    df["periodo_dia"] = pd.cut(
        df["hora"],
        bins=[0, 12, 18, 24],
        labels=["Manhã", "Tarde", "Noite"],
        right=False,
    )

    # Faixa de valor da venda
    df["faixa_valor"] = pd.cut(
        df["valor_total"],
        bins=[0, 100, 300, 600, float("inf")],
        labels=["Até 100", "100 a 300", "300 a 600", "Acima de 600"],
    )

    # Classificação da avaliação do cliente
    df["classificacao_avaliacao"] = pd.cut(
        df["avaliacao"],
        bins=[0, 6, 8, 10],
        labels=["Baixa", "Média", "Alta"],
        include_lowest=True,
    )

    print("Colunas derivadas criadas: ano, mes, nome_mes, dia_semana, hora, "
          "periodo_dia, faixa_valor, classificacao_avaliacao")
    return df

# Etapa 9: Arredondar valores (2 casas, igual ao NUMERIC do banco)

def arredondar(df):
    for coluna in COLUNAS_NUMERICAS:
        df[coluna] = df[coluna].round(2)
    return df

# Etapa 10: Salvar o CSV tratado

def salvar_csv(df):
    PASTA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_csv(CSV_TRATADO, index=False, encoding="utf-8")
    print(f"Base tratada salva em: {CSV_TRATADO}")


# Etapa 11: Gravar na tabela vendas_tratadas

def salvar_no_banco(df):
    # Só as colunas do dicionário de dados (as derivadas ficam no CSV)
    colunas_tabela = list(NOVOS_NOMES.values())
    engine = criar_conexao()
    with engine.begin() as conexao:
        conexao.execute(text("TRUNCATE TABLE vendas_tratadas"))
        df[colunas_tabela].to_sql(
            "vendas_tratadas", conexao, if_exists="append", index=False
        )
    print(f"{len(df)} linhas gravadas na tabela vendas_tratadas.")



if __name__ == "__main__":
    print("=" * 55)
    print("FASE 3 - ETL: LIMPEZA E TRANSFORMAÇÃO")
    print("=" * 55)

    dados = ler_dados()
    dados = renomear_colunas(dados)
    dados = limpar_textos(dados)
    dados = converter_tipos(dados)
    dados = tratar_nulos(dados)
    dados = remover_duplicados(dados)
    dados = validar_regras(dados)
    dados = criar_colunas_derivadas(dados)
    dados = arredondar(dados)

    print("\nTipos finais das colunas:")
    print(dados.dtypes)

    salvar_csv(dados)
    salvar_no_banco(dados)
