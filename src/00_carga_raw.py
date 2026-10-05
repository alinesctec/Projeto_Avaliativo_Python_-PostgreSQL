import pandas as pd
from sqlalchemy import text

from config import COLUNAS_RAW, CSV_ORIGINAL, criar_conexao



# Etapa 1: Ler o CSV original

def ler_csv_original():
    print("Lendo o arquivo:", CSV_ORIGINAL.name)
    df = pd.read_csv(CSV_ORIGINAL, sep=",", dtype=str)
    print(f"Linhas lidas: {len(df)} | Colunas: {len(df.columns)}")
    return df

# Etapa 2: Ajustar só o NOME das colunas para o padrão do banco

def renomear_colunas(df):
    return df.rename(columns=COLUNAS_RAW)

# Etapa 3: Gravar na tabela raw_vendas

def carregar_no_banco(df):
    engine = criar_conexao()

    with engine.begin() as conn:
        # Limpa a tabela antes, para poder rodar o script mais de uma vez
        conn.execute(text("TRUNCATE TABLE raw_vendas"))
        df.to_sql("raw_vendas", conn, if_exists="append", index=False)

    # Confere se a quantidade de linhas bate com o CSV
    with engine.connect() as conn:
        total = conn.execute(
            text("SELECT COUNT(*) FROM raw_vendas")
        ).scalar()

    print(f"Linhas na tabela raw_vendas: {total}")
    if total == len(df):
        print("OK! Todas as linhas do CSV foram carregadas.")
    else:
        print("ATENÇÃO: a quantidade de linhas não bate com o CSV!")

# Execução

if __name__ == "__main__":
    print("=" * 55)
    print("FASE 1 - CARGA DOS DADOS BRUTOS NO POSTGRESQL")
    print("=" * 55)

    dados = ler_csv_original()
    dados = renomear_colunas(dados)
    carregar_no_banco(dados)
