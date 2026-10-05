# Respostas às perguntas de negócio

Base analisada: **1000 vendas** de 01/01/2019
a 30/03/2019, em 3 filiais.
Faturamento total: **$ 322,966.82**.

## 1. Qual filial apresentou o maior faturamento?

- **Hipótese:** a filial com mais vendas também deve ter o maior faturamento.
- **Resposta:** **Giza**, com $ 110,568.71
  (34.2% do total).
- A diferença para a última colocada (Cairo) é de apenas
  $ 4,370.97, ou seja, as filiais estão bem equilibradas.

![Faturamento por filial](graficos/01_faturamento_por_filial.png)

## 2. Qual filial realizou a maior quantidade de vendas?

- **Hipótese:** é a mesma filial do maior faturamento.
- **Resposta:** **Alex**, com 340 vendas.
- Ticket médio por filial:
  Giza: $ 337.10, Alex: $ 312.35, Cairo: $ 319.87.
- Conclusão: a hipótese NÃO se confirmou: vender mais vezes não significa faturar mais, o ticket médio também pesa.

![Vendas por filial](graficos/02_vendas_por_filial.png)

## 3. Qual linha de produto apresentou o maior faturamento?

- **Resposta:** **Food and beverages**, com
  $ 56,144.86.
- Menor faturamento: Health and beauty
  ($ 49,193.81).

![Faturamento por linha](graficos/03_faturamento_por_linha.png)

## 4. Qual linha de produto recebeu a melhor avaliação média?

- **Hipótese:** a linha que mais fatura é a mais bem avaliada.
- **Resposta:** **Food and beverages**, com nota média 7.11.
- Pior avaliação: Home and lifestyle (6.84).
- A diferença entre a melhor e a pior nota é pequena
  (0.27 ponto).
- Conclusão: a hipótese se confirmou.

![Avaliação por linha](graficos/04_avaliacao_por_linha.png)

## 5. Qual foi a forma de pagamento mais utilizada?

- **Resposta:** **Ewallet**, usada em 345 vendas
  (34.5%).
- Distribuição:
  Ewallet: 345, Cash: 344, Credit card: 311.

![Formas de pagamento](graficos/05_formas_pagamento.png)

## 6. Qual foi o valor médio das vendas?

- **Resposta:** o valor médio foi **$ 322.97**.
- A mediana é $ 253.85. Como a média é maior que a mediana, existem
  algumas vendas de valor alto que puxam a média para cima.

![Distribuição do valor](graficos/06_distribuicao_valor_vendas.png)

## 7. Qual foi a maior venda registrada?

- **Resposta:** venda **860-79-0874**, no valor de
  **$ 1,042.65**, na filial Giza
  (Fashion accessories, 10 unidades de
  $ 99.30).

![Maiores vendas](graficos/07_maiores_vendas.png)

## 8. Em qual dia da semana ocorreu a maior quantidade de vendas?

- **Hipótese:** o fim de semana deve ter mais vendas.
- **Resposta:** **Sábado**, com 164 vendas.
- Dia com menos vendas: Segunda (125).
- Conclusão: a hipótese se confirmou só em parte. O sábado lidera, mas o
  domingo teve 133 vendas, abaixo de vários dias úteis.

![Vendas por dia](graficos/08_vendas_por_dia_semana.png)
