import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

from config import CSV_TRATADO, PASTA_GRAFICOS, PASTA_RESULTADOS

matplotlib.use("Agg")  # gera as imagens sem abrir janela

ORDEM_DIAS = ["Segunda", "Terça", "Quarta", "Quinta",
              "Sexta", "Sábado", "Domingo"]
COR = "#4C72B0"
COR_DESTAQUE = "#DD8452"


# Funções auxiliares

def moeda(valor):
    """Formata o número como dinheiro: 1234.5 -> $ 1,234.50"""
    return f"$ {valor:,.2f}"


def salvar_grafico(nome):
    plt.tight_layout()
    plt.savefig(PASTA_GRAFICOS / nome, dpi=100)
    plt.close()
    print(f"  Gráfico salvo: {nome}")


def grafico_barras(serie, titulo, eixo_y, nome_arquivo, horizontal=False):
    """Gráfico de barras com a maior barra destacada em laranja."""
    cores = [COR_DESTAQUE if v == serie.max() else COR for v in serie]
    plt.figure(figsize=(8, 5))
    if horizontal:
        plt.barh(serie.index, serie.values, color=cores)
        plt.xlabel(eixo_y)
        plt.gca().invert_yaxis()
    else:
        plt.bar(serie.index, serie.values, color=cores)
        plt.ylabel(eixo_y)
    plt.title(titulo)
    salvar_grafico(nome_arquivo)

# Etapa 1: Ler a base tratada

def ler_dados():
    df = pd.read_csv(CSV_TRATADO, parse_dates=["data_venda"])
    print(f"Base tratada carregada: {len(df)} vendas")
    return df

# Etapa 2: Estatística descritiva

def estatistica_descritiva(df):
    colunas = ["preco_unitario", "quantidade", "valor_total",
               "receita_bruta", "avaliacao"]
    tabela = df[colunas].describe().T
    tabela["mediana"] = df[colunas].median()
    tabela["moda"] = df[colunas].mode().iloc[0]
    tabela["amplitude"] = tabela["max"] - tabela["min"]
    tabela["coef_variacao_%"] = tabela["std"] / tabela["mean"] * 100
    tabela = tabela.round(2)

    tabela.to_csv(PASTA_RESULTADOS / "estatisticas_descritivas.csv")
    print("\nEstatística descritiva:")
    print(tabela)
    return tabela


# Etapa 3: Responder as perguntas de negócio

def pergunta_1_e_2_filiais(df):
    resumo = df.groupby("filial").agg(
        qtd_vendas=("id_venda", "count"),
        faturamento=("valor_total", "sum"),
        ticket_medio=("valor_total", "mean"),
    ).round(2).sort_values("faturamento", ascending=False)
    resumo.to_csv(PASTA_RESULTADOS / "resumo_filiais.csv")

    grafico_barras(resumo["faturamento"], "Faturamento por filial",
                   "Faturamento ($)", "01_faturamento_por_filial.png")
    grafico_barras(resumo["qtd_vendas"].sort_values(ascending=False),
                   "Quantidade de vendas por filial",
                   "Nº de vendas", "02_vendas_por_filial.png")
    return resumo


def pergunta_3_e_4_linhas(df):
    resumo = df.groupby("linha_produto").agg(
        qtd_vendas=("id_venda", "count"),
        faturamento=("valor_total", "sum"),
        avaliacao_media=("avaliacao", "mean"),
    ).round(2).sort_values("faturamento", ascending=False)
    resumo.to_csv(PASTA_RESULTADOS / "resumo_linhas_produto.csv")

    grafico_barras(resumo["faturamento"], "Faturamento por linha de produto",
                   "Faturamento ($)", "03_faturamento_por_linha.png",
                   horizontal=True)

    avaliacao = resumo["avaliacao_media"].sort_values(ascending=False)
    avaliacao.to_csv(PASTA_RESULTADOS / "resumo_avaliacao_linhas.csv")
    grafico_barras(avaliacao, "Avaliação média por linha de produto",
                   "Nota média (0 a 10)", "04_avaliacao_por_linha.png",
                   horizontal=True)
    return resumo


def pergunta_5_pagamento(df):
    resumo = df["forma_pagamento"].value_counts()
    resumo.to_csv(PASTA_RESULTADOS / "resumo_formas_pagamento.csv")

    plt.figure(figsize=(6, 6))
    plt.pie(resumo.values, labels=resumo.index, autopct="%1.1f%%",
            startangle=90, colors=[COR_DESTAQUE, COR, "#55A868"])
    plt.title("Formas de pagamento")
    salvar_grafico("05_formas_pagamento.png")
    return resumo


def pergunta_6_valor_medio(df):
    media = df["valor_total"].mean()
    mediana = df["valor_total"].median()

    plt.figure(figsize=(8, 5))
    plt.hist(df["valor_total"], bins=20, color=COR, edgecolor="white")
    plt.axvline(media, color="red", linestyle="--",
                label=f"Média: {moeda(media)}")
    plt.axvline(mediana, color="green", linestyle="--",
                label=f"Mediana: {moeda(mediana)}")
    plt.title("Distribuição do valor das vendas")
    plt.xlabel("Valor da venda ($)")
    plt.ylabel("Quantidade de vendas")
    plt.legend()
    salvar_grafico("06_distribuicao_valor_vendas.png")
    return media, mediana


def pergunta_7_maior_venda(df):
    top10 = df.nlargest(10, "valor_total")[
        ["id_venda", "filial", "linha_produto", "quantidade",
         "preco_unitario", "valor_total", "data_venda"]
    ]
    top10.to_csv(PASTA_RESULTADOS / "resumo_top10_vendas.csv", index=False)

    serie = top10.set_index("id_venda")["valor_total"]
    grafico_barras(serie, "As 10 maiores vendas", "Valor da venda ($)",
                   "07_maiores_vendas.png", horizontal=True)
    return top10.iloc[0]


def pergunta_8_dia_semana(df):
    resumo = df["dia_semana"].value_counts().reindex(ORDEM_DIAS)
    resumo.to_csv(PASTA_RESULTADOS / "resumo_dias_semana.csv")
    grafico_barras(resumo, "Quantidade de vendas por dia da semana",
                   "Nº de vendas", "08_vendas_por_dia_semana.png")
    return resumo


# Etapa 4: Escrever o arquivo de respostas

def escrever_respostas(df, filiais, linhas, pagamento, media, mediana,
                       maior, dias):
    fat = filiais["faturamento"]
    qtd = filiais["qtd_vendas"]
    aval = linhas["avaliacao_media"].sort_values(ascending=False)
    total = len(df)

    texto = f"""# Respostas às perguntas de negócio

Base analisada: **{total} vendas** de {df['data_venda'].min():%d/%m/%Y}
a {df['data_venda'].max():%d/%m/%Y}, em {df['filial'].nunique()} filiais.
Faturamento total: **{moeda(df['valor_total'].sum())}**.

## 1. Qual filial apresentou o maior faturamento?

- **Hipótese:** a filial com mais vendas também deve ter o maior faturamento.
- **Resposta:** **{fat.idxmax()}**, com {moeda(fat.max())}
  ({fat.max() / fat.sum():.1%} do total).
- A diferença para a última colocada ({fat.idxmin()}) é de apenas
  {moeda(fat.max() - fat.min())}, ou seja, as filiais estão bem equilibradas.

![Faturamento por filial](graficos/01_faturamento_por_filial.png)

## 2. Qual filial realizou a maior quantidade de vendas?

- **Hipótese:** é a mesma filial do maior faturamento.
- **Resposta:** **{qtd.idxmax()}**, com {qtd.max()} vendas.
- Ticket médio por filial:
  {", ".join(f"{f}: {moeda(v)}" for f, v in filiais["ticket_medio"].items())}.
- Conclusão: {"a hipótese se confirmou" if qtd.idxmax() == fat.idxmax()
              else "a hipótese NÃO se confirmou: vender mais vezes não "
                   "significa faturar mais, o ticket médio também pesa"}.

![Vendas por filial](graficos/02_vendas_por_filial.png)

## 3. Qual linha de produto apresentou o maior faturamento?

- **Resposta:** **{linhas['faturamento'].idxmax()}**, com
  {moeda(linhas['faturamento'].max())}.
- Menor faturamento: {linhas['faturamento'].idxmin()}
  ({moeda(linhas['faturamento'].min())}).

![Faturamento por linha](graficos/03_faturamento_por_linha.png)

## 4. Qual linha de produto recebeu a melhor avaliação média?

- **Hipótese:** a linha que mais fatura é a mais bem avaliada.
- **Resposta:** **{aval.index[0]}**, com nota média {aval.iloc[0]:.2f}.
- Pior avaliação: {aval.index[-1]} ({aval.iloc[-1]:.2f}).
- A diferença entre a melhor e a pior nota é pequena
  ({aval.iloc[0] - aval.iloc[-1]:.2f} ponto).
- Conclusão: {"a hipótese se confirmou" if aval.index[0] == linhas[
    'faturamento'].idxmax() else "a hipótese NÃO se confirmou"}.

![Avaliação por linha](graficos/04_avaliacao_por_linha.png)

## 5. Qual foi a forma de pagamento mais utilizada?

- **Resposta:** **{pagamento.idxmax()}**, usada em {pagamento.max()} vendas
  ({pagamento.max() / total:.1%}).
- Distribuição:
  {", ".join(f"{k}: {v}" for k, v in pagamento.items())}.

![Formas de pagamento](graficos/05_formas_pagamento.png)

## 6. Qual foi o valor médio das vendas?

- **Resposta:** o valor médio foi **{moeda(media)}**.
- A mediana é {moeda(mediana)}. Como a média é maior que a mediana, existem
  algumas vendas de valor alto que puxam a média para cima.

![Distribuição do valor](graficos/06_distribuicao_valor_vendas.png)

## 7. Qual foi a maior venda registrada?

- **Resposta:** venda **{maior['id_venda']}**, no valor de
  **{moeda(maior['valor_total'])}**, na filial {maior['filial']}
  ({maior['linha_produto']}, {maior['quantidade']} unidades de
  {moeda(maior['preco_unitario'])}).

![Maiores vendas](graficos/07_maiores_vendas.png)

## 8. Em qual dia da semana ocorreu a maior quantidade de vendas?

- **Hipótese:** o fim de semana deve ter mais vendas.
- **Resposta:** **{dias.idxmax()}**, com {dias.max()} vendas.
- Dia com menos vendas: {dias.idxmin()} ({dias.min()}).
- Conclusão: a hipótese se confirmou só em parte. O sábado lidera, mas o
  domingo teve {dias['Domingo']} vendas, abaixo de vários dias úteis.

![Vendas por dia](graficos/08_vendas_por_dia_semana.png)
"""
    caminho = PASTA_RESULTADOS / "respostas_negocio.md"
    caminho.write_text(texto, encoding="utf-8")
    print(f"\nRespostas salvas em: {caminho}")
    print(texto)

if __name__ == "__main__":
    print("=" * 55)
    print("FASE 4 - ESTATÍSTICA E PERGUNTAS DE NEGÓCIO")
    print("=" * 55)

    PASTA_GRAFICOS.mkdir(parents=True, exist_ok=True)

    dados = ler_dados()
    estatistica_descritiva(dados)

    print("\nGerando gráficos...")
    res_filiais = pergunta_1_e_2_filiais(dados)
    res_linhas = pergunta_3_e_4_linhas(dados)
    res_pagamento = pergunta_5_pagamento(dados)
    valor_medio, valor_mediana = pergunta_6_valor_medio(dados)
    maior_venda = pergunta_7_maior_venda(dados)
    res_dias = pergunta_8_dia_semana(dados)

    escrever_respostas(dados, res_filiais, res_linhas, res_pagamento,
                       valor_medio, valor_mediana, maior_venda, res_dias)
