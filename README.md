# Projeto Rossmann
<img src="img/rossmann_banner.jpg" alt="drawing" width="900" height="400"/>


## Problema de negócio.
O Chief Financial Officer ( CFO ) da rede farmacêutica Rossmann, precisa determinar como ele distribuirá o orçamento para reforma para as lojas da rede, no entanto ele ainda não sabe qual será o orçamento disponível. Portanto o CFO precisa determinar qual é orçamento esperado para cada uma das lojas da Rossmann no próximo intervalo de 6 semanas e com esses dados separar uma parte do valor total esperado de arrecadamento para realizar as reformas.


## Premissas do negócio
A Rossmann opera mais de 3000 farmácias em 7 países europeus. Atualmente, os gerentes das lojas receberam a tarefa de prever a soma das vendas diárias de sua loja nas próximas 6 semanas. As vendas de cada loja são influenciadas por muitos fatores, incluindo promoções, competição, feriados estaduais e escolares, sazonalidade e localização.

<details>
    <summary><b>Dados referentas as lojas</b></summary>

|   |   |
|---|---|
| **Store** | Id único para representar cada loja. |
| **StoreType** | Diferencia as lojas em 4 tipos: (a, b, c, d) |
| **Assortment** | Descreve a loja em uma de 3 diferentes classes: (a - basic, b - extra, c - extended) |
| **Competition Distance** | Distância em metros da loja competidora mais próxima. |
| **CompetionOpen SinceMonth** | Mês em que o competidor mais próximo foi aberta. |
| **CompetitionOpen SinceYear** | Ano em que o competidor mais próximo foi aberta. <br/>(ao combinarmos com o dado acima, obtemos a data de abertura do competidor mais próximo à loja em questão) |
| **Promo2** | Promoção recorrente que algumas lojas participam, a qual acontece em certos meses fixos do ano. <br/>(0 - Loja não participa, 1 - Loja participa) |
| **Promo2Since Week** | Indica a semana do ano em que a loja começou a participar da Promo2. |
| **Promo2Since Year** | Indica o ano que a Promo2 foi implementada nessa loja (caso tenha sido). |
| **PromoInterval** | Indica os meses do ano em que a Promo2 fica ativa. (caso a loja participe) |
</details>

<br/>

<details>
    <summary><b>Dados referentes as vendas</br></summary>

|   |   |
|---|---|
| **Store** | Id único para representar cada loja |
| **DayOfWeek** | Número de 1 a 7 para representar o dia da semana. <br/>(1 - Segunda-feira, … , 7 - Domingo) |
| **Date** | Data em que cada registro dessa tabela foi coletado. |
| **Sales** | Valor arrecadado no dia. |
| **Customers** | Número de clientes que compraram naquele dia. |
| **Open** | Indica se a loja estava aberta. <br/>(0 - Fechada, 1 - Aberta) |
| **Promo** | Indica se naquele dia havia alguma promoção ativa. <br/>(0 - Não, 1 - Sim) |
| **StateHoliday** | Indica se há um feriado estadual. Normalmente, as lojas são fechadas nessas ocasiões. <br/>(a - Public holiday, b - Easter holiday, c - Christmas, 0 - None) |
| **SchoolHoliday** | Indica se a loja foi afetada pela fechamento das escolas. <br/>(0 - Não, 1 - Sim) |
</details>


## Estratégia da solução.
Esse projeto foi realizado seguindo os passos do método CRISP-DS.

1. **Problema de Negócios:**
2. **Entendimento de Negócio:**
3. **Coleta de Dados:**
4. **Limpeza dos Dados:**
5. **Exploração dos Dados:**
6. **Modelagem dos Dados:**
7. **Aplicação de Algoritmos de Machine Learning:**
8. **Avaliação de Performance:**
9. **Publicação da Solução:**

## Top 3 Insights de dados.
<img src="img/MindMapHypothesis.png" alt="drawing" width="800" height="600"/>

## Modelos de Machine Learning.
<img src="img/time_series_CV.png" alt="drawing"/>

## O produto final do projeto.
<img src="img/bot_telegram.png" alt="drawing"/>

<video width="800" height="500" controls>
  <source src="img/telebot_test.mp4" type="video/mp4">
</video>

## Conclusão.
## Próximos passos.