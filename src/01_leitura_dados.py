import io

import pandas as pd

from config import CSV_EXPORTADO, PASTA_RESULTADOS

# Etapa 1: Ler o CSV exportado

def ler_dados():
    df = pd.read_csv(CSV_EXPORTADO, sep=",")
    return df

# Etapa 2: Inspecionar os dados

def inspecionar(df):
    linhas = []  

    def titulo(texto):
        linhas.append("")
        linhas.append("=" * 55)
        linhas.append(texto)
        linhas.append("=" * 55)

    titulo("1. TAMANHO DA BASE")
    linhas.append(f"Linhas: {df.shape[0]}")
    linhas.append(f"Colunas: {df.shape[1]}")

    titulo("2. PRIMEIRAS LINHAS")
    linhas.append(df.head().to_string())

    titulo("3. TIPOS DAS COLUNAS (df.info)")
    buffer = io.StringIO()
    df.info(buf=buffer)
    linhas.append(buffer.getvalue())

    titulo("4. VALORES NULOS POR COLUNA")
    linhas.append(df.isnull().sum().to_string())
    linhas.append(f"Total de nulos: {df.isnull().sum().sum()}")

    titulo("5. LINHAS DUPLICADAS")
    linhas.append(f"Linhas duplicadas: {df.duplicated().sum()}")
    linhas.append(
        f"Códigos de venda repetidos: {df['invoice_id'].duplicated().sum()}"
    )

    titulo("6. VALORES ÚNICOS DAS COLUNAS DE TEXTO")
    for coluna in ["branch", "city", "customer_type", "gender",
                   "product_line", "payment"]:
        valores = sorted(df[coluna].unique())
        linhas.append(f"{coluna}: {valores}")

    titulo("7. ESTATÍSTICAS BÁSICAS (df.describe)")
    linhas.append(df.describe().round(2).to_string())

    titulo("8. INCONSISTÊNCIAS ENCONTRADAS")
    linhas.append(
        "- A coluna 'date' está como texto (object) no formato mês/dia/ano."
    )
    linhas.append("- A coluna 'time' está como texto no formato 12h (AM/PM).")
    linhas.append("- Os nomes das colunas estão em inglês.")
    linhas.append("- Valores com muitas casas decimais (ex: 26.1415).")
    linhas.append(
        "- 'gross_margin_percentage' tem o mesmo valor em todas as linhas."
    )

    return "\n".join(linhas)



# Etapa 3: Mostrar e salvar o relatório

def salvar_relatorio(texto):
    PASTA_RESULTADOS.mkdir(parents=True, exist_ok=True)
    caminho = PASTA_RESULTADOS / "01_relatorio_inspecao.txt"
    caminho.write_text(texto, encoding="utf-8")
    print(f"\nRelatório salvo em: {caminho}")


# Execução

if __name__ == "__main__":
    print("=" * 55)
    print("LEITURA E INSPEÇÃO INICIAL DOS DADOS")
    print("=" * 55)

    dados = ler_dados()
    relatorio = inspecionar(dados)
    print(relatorio)
    salvar_relatorio(relatorio)
