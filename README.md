# House Rocket Company

![1](/images/city.jpg "Image Title")



## Story Telling

A House Rocket é uma empresa ficticia do ramo imobiliário que atua na compra e venda de imoveis em King Country nos Estados Unidos. Um dos desafios desse ramo é estar atendo as principais oportunidades, como cientista de dados nosso trabalho é atraves de ferramentas matemáticas e da computação descobrir essas oportunidades e densenvolver soluções inteligentes. Objetivo é entender o modelo de negócio da empresa e atraves de analises construir um dashboard ( graficos, tabelas, mapas iterativos..) que contem as principais caracteristicas necessárias para uma tomada de decisão do time de negócios. Em seguida será desenvolvido um modelo de machine learning capaz de fazer predições sobre o preço dos imoveis.

*Essa base de dados e o glossário estão diponíveis no [Geocenter](https://geodacenter.github.io/data-and-lab/KingCounty-HouseSales2015/).*

## Business Approach

Dado o contexto o CEO da House Rocket fez os seguintes questionamentos:

* Quais imóveis deveria comprar e por qual preço de compra?
* Quando deveria vender os imóveis?
* O plano de ação da empresa é satisfatório? o que a solução de machine learning agregaria a empresa?

## Etapas de Desenvolvimento

* Entendimento do Negócio
* Coleta dos dados 
* Preparação dos dados
* Analise Exploratória dos dados 
* Desenvolvimento do modelo
* Implementação

Exemplo de um dos gráficos gerados na analise exploratória:

![4](/images/grades.png)
<br>*O preço da casa cresce exponencialmente com o nivel da arquitetura do imovel, quanto a nivel da arquitetura aumenta mais o preço do imovel varia. Em outras analises é possivel perceber que a arquitetura influencia mais no preço do imovel do que seu estado de concervação.*

Todas essas etapas estão e analises estão mais detalhadas e diponiveis na pasta notebook <u>house_sales.ipynb</u>

## Insights
Principais insights gerados no projeto:

* Sobre o negócio:
    - A condição do imóvel possui um efeito significamente menor no preço do imóvel quando comparado ao "grade" ( nivel da arquitura, estética...) do imovel
    - Maior parte dos imóveis estão localizados ao norte de King Country
    - Os imóveis mais caros estão proximos a Lake Washington.
    - Imoveis novos ( menos de 15 anos de construção) são em média 19.01% mais caros.
* Retorno Financeiro:
    - Seguindo a estrátégia de negócio atual da empresa foram encontrados aproximadamente 2500 potênciais imoveis para compra, o que representa um potencial lucro de 1,5bilhões de dolares nas revendas.    

## Produto Final

 - O dashboard está hospedado na nuvem do heroku, clique no [link](https://house-rocket-75.herokuapp.com/) para acessar.

***

## Ferramentas

* Linguagens: Python
* IDE: Visual Studio Code, Jupyter Notebook
* Bibliotecas: Pandas, Seaborn, Folium, Altair, Geopandas, Sklearn
* Frameworks: Streamlit(Dashboard)
* Deploy: Heroku
* Ferramentas Adiocionais: Docker
* Metodologia: CRISP-DM






