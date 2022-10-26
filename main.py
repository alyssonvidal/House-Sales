import streamlit as st


st.set_page_config(page_title='House Rocket', layout='wide')

def main():
    
    st.title( 'House Rocket Company' )    
    st.caption( 'Welcome to House Rocket Data Analysis')
    st.image("images/logo.png", width=300)
    st.header( 'Sumary')
    st.markdown( '''
    A House Rocket Company é uma empresa ficticia que trabalha com compras e reventas de imoveis na região de Seattle, EUA.
    Objetivo desse projeto é conseder a um dashboard ( graficos, tabelas, mapas iterativos..) que contem as principais caracteristicas necessárias para uma tomada de decisão do time de negócios.
    
    **Credit:** App built in `Python` + `Streamlit` by [Alysson Machado](https://www.linkedin.com/in/alyssonmach/).
    ''')

    st.subheader( 'Usage')
    st.markdown( ''' 
    * Trabalhar com tabelas iterativas com filtros específicos, analises estátiticas resumidas e metricas de desempenho.
    * Trabalhar com graficos iterativos'
    * Trabalhar com mapas iterativos, com seleção das areas por codigo postal, preço/area entre outro
    * Ter acesso as recomendaçõs dos imóveis de acordo com as métricas adotadas da empresa
    * Modelo de regressão de machine learning capaz de fazer predições sobre o preço dos imóveis *(...coming soon)*
    ''')

if __name__ == "__main__": 
    main()    




