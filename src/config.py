
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine


# 1. Caminhos das pastas

PASTA_PROJETO = Path(__file__).resolve().parent.parent
PASTA_RAW = PASTA_PROJETO / "data" / "raw"
PASTA_PROCESSED = PASTA_PROJETO / "data" / "processed"
PASTA_RESULTADOS = PASTA_PROJETO / "resultados"
PASTA_GRAFICOS = PASTA_RESULTADOS / "graficos"

# Arquivos usados no pipeline
CSV_ORIGINAL = PASTA_RAW / "SuperMarketAnalysis.csv"
CSV_EXPORTADO = PASTA_RAW / "vendas_exportadas.csv"
CSV_TRATADO = PASTA_PROCESSED / "vendas_tratadas.csv"


# 2. Nomes das colunas na camada Raw

COLUNAS_RAW = {
    "Invoice ID": "invoice_id",
    "Branch": "branch",
    "City": "city",
    "Customer type": "customer_type",
    "Gender": "gender",
    "Product line": "product_line",
    "Unit price": "unit_price",
    "Quantity": "quantity",
    "Tax 5%": "tax_5_percent",
    "Sales": "sales",
    "Date": "date",
    "Time": "time",
    "Payment": "payment",
    "cogs": "cogs",
    "gross margin percentage": "gross_margin_percentage",
    "gross income": "gross_income",
    "Rating": "rating",
}


# 3. Conexão com o PostgreSQL

load_dotenv(PASTA_PROJETO / ".env")

USUARIO = os.getenv("SM_USUARIO", "postgres")
SENHA = os.getenv("SM_SENHA", "")
HOST = os.getenv("SM_HOST", "localhost")
PORTA = os.getenv("SM_PORTA", "5432")
BANCO = os.getenv("SM_BANCO", "base_supermarket")


def criar_conexao():
    """Cria e devolve a conexão (engine) com o PostgreSQL."""
    url = f"postgresql+psycopg2://{USUARIO}:{SENHA}@{HOST}:{PORTA}/{BANCO}"
    return create_engine(url)
