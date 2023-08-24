#============================ PROJETO ALUNO ====================================#

#Importação das Bibliotecas

import pandas as pd
import numpy as np
import inflection
import streamlit as st
import plotly.express as px

#Importação do dataset
df = pd.read_csv('zomato.csv')

st.set_page_config(page_title="Visão Restaurante",page_icon="🍽️")

#========================== TRATAMENTO DOS DADOS ===============================#


#Cópia do dataframe
df1 = df.copy()

#Excluir as linhas com valores vazios 
df1 = df1.dropna()



#===================================== FUNÇÕES =================================#



def restaurant_votes_or_rating(df1,x):
    '''Retorna um dataframe com a maior quantidade de avaliações ou
    a maior média por Restaurante'''
    if x=="votes":
        df_aux = (df1.loc[:,["restaurant_name","votes"]]
                     .groupby(["restaurant_name"])
                     .sum()
                     .sort_values("votes",ascending=False)
                     .reset_index())
    if x=="rating":
        df_aux = (df1.loc[:,["restaurant_name","aggregate_rating"]]
                     .groupby(["restaurant_name"])
                     .mean()
                     .sort_values("aggregate_rating",ascending=False)
                     .reset_index())
    else:
        print("Erro")

    return df_aux


def restaurant_delivery_votes(df1):
#Retorna um gráfico que contém a média de avaliações de restaurantes que fazem entregas e os que não fazem
    df_aux1 = (df1.loc[df1["has_online_delivery"]==1,["has_online_delivery","restaurant_name","votes"]]
                  .groupby(["has_online_delivery","restaurant_name"])
                  .count().sort_values("votes",ascending=False)
                  .reset_index())
    
    df_aux2 = (df1.loc[df1["has_online_delivery"]==0,["has_online_delivery","restaurant_name","votes"]]
                  .groupby(["has_online_delivery","restaurant_name"])
                  .count()
                  .sort_values("votes",ascending=False)
                  .reset_index())
        
    df3 = (pd.concat([df_aux1,df_aux2])
                     .reset_index(drop=True))
    
    df3 = (df3.loc[:,["has_online_delivery","votes"]]
              .groupby(["has_online_delivery"])
              .mean()
              .reset_index())
        
    for i in range(len(df3)):
        if (df3.loc[i,"has_online_delivery"]==0):
            df3.loc[i,"has_online_delivery"]="Não faz entrega online"
    
        if (df3.loc[i,"has_online_delivery"]==1):
            df3.loc[i,"has_online_delivery"]="Faz entrega online"
                    
    fig = px.bar( df3, x='has_online_delivery', y='votes')

    return fig

def restaurant_brazilian(df1):
        #Retorna um dataframe com os restaurante de culinária 'Brazilian' com pior nota média
        df_aux = (df1.loc[(df1["cuisines"]=="Brazilian"),["restaurant_name","aggregate_rating"]]
                     .groupby(["restaurant_name"])
                     .mean()
                     .sort_values("aggregate_rating",ascending=True)
                     .reset_index())
        return df_aux


def restaurant_for_two(df1):
    #Retorna um dataframe com o maior valor de um prato para duas pessoas por restaurante
    df_aux = (df1.loc[:,["restaurant_name","average_cost_for_two"]]
                 .groupby(["restaurant_name"])
                 .max()
                 .sort_values("average_cost_for_two",ascending=False)
                 .reset_index())
    return df_aux


def restaurant_table_for_two(df1):
            #Retorna um gráfico com o maior valor médio de um prato para duas pessoas em restaurantes com e sem reserva
            df_aux1 = (df1.loc[df1["has_table_booking"]==1,["has_table_booking","restaurant_name","average_cost_for_two"]]
                          .groupby(["restaurant_name"])
                          .mean()
                          .sort_values("average_cost_for_two",ascending=False)
                          .reset_index())
    
            df_aux2 = (df1.loc[df1["has_table_booking"]==0,["has_table_booking","restaurant_name","average_cost_for_two"]]
                          .groupby(["restaurant_name"])
                          .mean() 
                          .sort_values("average_cost_for_two",ascending=False)
                          .reset_index())
    
            df3 = (pd.concat([df_aux1,df_aux2])
                 .reset_index(drop=True))
    
            df3 = (df3.loc[:,["has_table_booking","average_cost_for_two"]]
                      .groupby(["has_table_booking"])
                      .mean()
                      .reset_index())
    
    
            for i in range(len(df3)):
                if (df3.loc[i,"has_table_booking"]==0):
                    df3.loc[i,"has_table_booking"]="Não tem reserva"
    
                if (df3.loc[i,"has_table_booking"]==1):
                    df3.loc[i,"has_table_booking"]="Tem reserva"
        
            fig = px.bar( df3, x='has_table_booking', y='average_cost_for_two')
            return fig


def restaurant_japanese_bbq_for_two(df1):
            '''Retorna um dataframe com o valor médio de prato para duas pessoas em restaurante do tipo de culinária japonesa dos estados unidos e de churrascarias americanas'''
            
            df1_japanese = df1[(df1["cuisines"] == "Japanese") & (df1["country_code"] == 216)]
            df1_bbq = df1[df1["cuisines"] == "BBQ"]
    
        
            avg_cost_japanese = df1_japanese["average_cost_for_two"].mean()
            avg_cost_bbq = df1_bbq["average_cost_for_two"].mean()
        
            # Criar um DataFrame com os resultados
            data = {
                "Culinária": ["Japonesa", "BBQ (Churrascaria)"],
                "Valor Médio": [avg_cost_japanese, avg_cost_bbq]
            }
            df_aux = pd.DataFrame(data)
            return df_aux
#Preenchimento do nome dos países
COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}

def country_name(country_id):
    return COUNTRIES[country_id]


#Preenchimento do código dos países
paises = {
    "India": 1,
    "Australia": 14,
    "Brazil": 30,
    "Canada": 37,
    "Indonesia": 94,
    "New Zealand": 148,
    "Philippines": 162,
    "Qatar": 166,
    "Singapore": 184,
    "South Africa": 189,
    "Sri Lanka": 191,
    "Turkey": 208,
    "United Arab Emirates": 214,
    "England": 215,
    "United States of America": 216,}

def numero_paises(country_names):
    #Necessária alteração para que o filtro aceite uma lista de parâmetros
    country_codes = []
    
    for country_name in country_names:
        if country_name in paises:
            codes = paises[country_name]
            country_codes.append(codes)
    
    return country_codes



#Criação do Tipo de Categoria de Comida

def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"


#Criação do nome das Cores
COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}

def color_name(color_code):
    return COLORS[color_code]


#Renomear as colunas do DataFrame

def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df


df1 = rename_columns(df1)


#Categorizar todos os restaurantes somente por um tipo de culinária

# Função para obter o primeiro elemento após o split
def get_first_cuisine(cuisines):
    return cuisines.split(",")[0] if isinstance(cuisines, str) else cuisines

# Aplicando a função na coluna "Cuisines"
df1["cuisines"] = df1["cuisines"].apply(get_first_cuisine)




#============================ BARRA LATERAL ====================================#




#Cria a barrinha de separação

st.sidebar.header("Fome Zero")

st.sidebar.markdown("""---""")

st.sidebar.header("Filtros")

st.sidebar.markdown("""---""")


#Filtro de países
country_options = st.sidebar.multiselect("Selecione os países os quais deseja obter informções:",["United States of America","England","United Arab Emirates","Brazil","India","Canada"],default=["United States of America","England","United Arab Emirates","Brazil","India","Canada"])

   
# A função isin() é usada para filtrar dados em um DataFrame ou Series com base em uma lista de valores. Ela retorna uma máscara booleana indicando quais elementos estão presentes na lista fornecida.
    
linhas_selecionadas = df1["country_code"].isin(numero_paises(country_options))
df1 = df1.loc[linhas_selecionadas,:]


#============================ VISÃO RESTAURANTE ====================================#

st.header("🍽️Visão Restaurante")

tab1,tab2 = st.tabs(["Geral","Visão a par"])

with tab1:
    with st.container():

        col1,col2 = st.columns(2)

        with col1:
            
            #Qual o nome do restaurante que possui a maior quantidade de avaliações?
            df_aux = restaurant_votes_or_rating(df1,"votes")
            nome = df_aux.loc[0,"restaurant_name"]
            avaliacoes = df_aux.loc[0,"votes"]
    
            col1.metric("Maior em avaliações:",avaliacoes)
            st.markdown(f"<p><strong>Restaurante:</strong> {nome}</p>", unsafe_allow_html=True)
        
    

        with col2:
            #Qual o nome do restaurante com a maior nota média?
            df_aux = restaurant_votes_or_rating(df1,"rating")
            nome = df_aux.loc[0,"restaurant_name"]
            nota = df_aux.loc[0,"aggregate_rating"]

            col2.metric("Maior nota média:",nota)
            st.markdown(f"<p><strong>Restaurante:</strong> {nome}</p>", unsafe_allow_html=True)

    

    with st.container():    
        #Os restaurantes que aceitam pedido online são também, na média, os restaurantes que mais possuem avaliações registradas?
        st.markdown("""---""")
        st.header("Média de avaliações com ou sem entrega dos restaurantes")
    
        fig = restaurant_delivery_votes(df1)
        st.plotly_chart(fig,use_container_width=True)


        
        #Qual o nome do restaurante de tipo de culinária brasileira que possui a menor média de avaliação?
        df_aux = restaurant_brazilian(df1)
        nome = df_aux.loc[0,"restaurant_name"]
        media = df_aux.loc[0,"aggregate_rating"]

        st.markdown("""---""")
        st.markdown("<h3 style='text-align: center;'>Culinária brasileira que possui a menor média de avaliação</h3>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Restaurante:</strong> {nome}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Avaliações feitas:</strong> {media}</p>", unsafe_allow_html=True)



with tab2:
    with st.container():
        #Qual o nome do restaurante que possui o maior valor de uma prato para duas pessoas?
        df_aux = restaurant_for_two(df1)
        nome = df_aux.loc[0,"restaurant_name"]
        valor = df_aux.loc[0,"average_cost_for_two"]

    
        st.markdown("<h3 style='text-align: center;'>Restaurante que possui o maior valor de uma prato para duas pessoas</h3>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Restaurante:</strong> {nome}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Avaliações feitas:</strong> {valor}</p>", unsafe_allow_html=True)


        
        #Os restaurantes que fazem reservas são também, na média, os restaurantes que possuem o maior valor médio de um prato para duas pessoas?
        st.markdown("""---""")
        st.header("Média de um prato para duas pessoas ")
        fig = restaurant_table_for_two(df1)
        st.plotly_chart(fig,use_container_width=True)


        
        #Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América possuem um valor médio de prato para duas pessoas maior que as churrascarias americanas (BBQ)?
        st.markdown("""---""")
        st.header("Média de um prato para duas pessoas da culinária japonesa nos EUA e suas churrascarias")
        st.dataframe(restaurant_japanese_bbq_for_two(df1))