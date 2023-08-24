#============================ PROJETO ALUNO ====================================#

#Importação das Bibliotecas

import pandas as pd
import numpy as np
import inflection
import streamlit as st
import plotly.express as px

#Importação do dataset
df = pd.read_csv('zomato.csv')

st.set_page_config(page_title="Visão Cidade",page_icon="🏢")


#========================== TRATAMENTO DOS DADOS ===============================#


#Cópia do dataframe
df1 = df.copy()

#Excluir as linhas com valores vazios 
df1 = df1.dropna()


#===================================== FUNÇÕES =================================#



def city_registered(df1):
    #Me retorna um dataframe com a ordem das cidades com mais restaurantes registrados
    df_aux = (df1.loc[:,["restaurant_id","city"]]
                 .groupby(["city"])
                 .count()
                 .sort_values("restaurant_id",ascending=False)
                 .reset_index())
    return df_aux


def for_two_city(df1):
    #Me retorna um dataframe em ordem das cidades que possui o maior valor médio de um prato para dois
    df_aux = (df1.loc[:,["average_cost_for_two","city"]]
                 .groupby(["city"])
                 .mean()
                 .sort_values("average_cost_for_two",ascending=False)
                 .reset_index())
    return df_aux


def cuisines_distinct(df1):
    #Me retorna um dataframe em ordem das cidades que possui maior quantidade de culinárias distintas
    df_aux =(df1.loc[:,["cuisines","city"]]
                .groupby(["city"])
                .nunique()
                .sort_values("cuisines",ascending=False)
                .reset_index())
    return df_aux


def avg_4(df1):
    #Me retorna um gráfico com as 10 cidades que possuem mais restaurantes com nota média acima de 4
    df_1 = (df1.loc[df1["aggregate_rating"]>4,["restaurant_id","city"]]
               .groupby(["city"])
               .count()
               .sort_values("restaurant_id",ascending=False)
               .reset_index())
    
    df_aux = df_1.loc[0:10,:]
    fig = px.bar(df_aux,x="city",y="restaurant_id")    
    return fig


def avg_2_5(df1):
    #Me retorna um gráfico com as 10 cidades que possuem mais restaurantes com nota média abaixo de 2.5
    df_1 = (df1.loc[df1["aggregate_rating"]<2.5,["restaurant_id","city"]]
               .groupby(["city"])
               .count()
               .sort_values("restaurant_id",ascending=False)
               .reset_index())
        
    df_aux = df_1.loc[0:10,:]
    fig = px.bar(df_aux,x="city",y="restaurant_id")
    
    return fig


def delivery_city(df1):
    #Me possa um dataframe em ordem das cidades que mais possuem restaurantes que aceitam pedidos online
    df_aux = (df1.loc[df1["has_online_delivery"]==1,["city","restaurant_id"]]
                 .groupby(["city"])
                 .count()
                 .sort_values("restaurant_id",ascending=False)
                 .reset_index())
    return df_aux



    
def table_or_delivering(df1,x):
    '''Me retorna um dataframe que contém em ordem as cidades com maior quantidade de restaurantes
    que fazem reservas e que fazem entregas, basta passar como parâmetros o dataframe e indicando 
    se é table(Para reservas) ou delivering(Para entregas)'''
    if x=="table":
        df_aux = (df1.loc[df1["has_table_booking"]==1,["city","restaurant_id"]]
                     .groupby(["city"])
                     .count()
                     .sort_values("restaurant_id",ascending=False)
                     .reset_index())
    if x=="delivering":
        df_aux = (df1.loc[df1["is_delivering_now"]==1,["city","restaurant_id"]]
                     .groupby(["city"])
                     .count()
                     .sort_values("restaurant_id",ascending=False)
                     .reset_index())
    
    else:
        print("Erro")

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


st.sidebar.header("Fome Zero")

#Cria a barrinha de separação
st.sidebar.markdown("""---""")

st.sidebar.header("Filtros")

st.sidebar.markdown("""---""")


#Filtro de países
country_options = st.sidebar.multiselect("Selecione os países os quais deseja obter informções:",["United States of America","England","United Arab Emirates","Brazil","India","Canada"],default=["United States of America","England","United Arab Emirates","Brazil","India","Canada"])

   
# A função isin() é usada para filtrar dados em um DataFrame ou Series com base em uma lista de valores. Ela retorna uma máscara booleana indicando quais elementos estão presentes na lista fornecida.
    
linhas_selecionadas = df1["country_code"].isin(numero_paises(country_options))
df1 = df1.loc[linhas_selecionadas,:]



#Filtro slider

range = st.sidebar.slider("Faixa de preço dos restaurantes:", min_value=1, max_value=4, value=4)

linhas_selecionadas = df1["price_range"]<=range
df1 = df1.loc[linhas_selecionadas,:]

#Is delivering now	
#st.sidebar.markdown("""---""")
#opcoes = ["Está entregando agora", "Não está entregando agora"]

#status_entrega = st.sidebar.radio("Selecione uma opção de entrega:", opcoes)

#if status_entrega=="Está entregando agora":
 #   df1 = df1.loc[df1["is_delivering_now"]==1,:]

#else:
 #   df1 = df1.loc[df1["is_delivering_now"]==0,:]

#============================ VISÃO CIDADE ====================================#

st.header("🏢Visão Cidade")

tab1,tab2,tab3 = st.tabs(["Geral","Métricas","Serviços"])

with tab1:
    with st.container():        
        #Qual o nome da cidade que possui mais restaurantes registrados?
        df_aux = city_registered(df1)
        nome= df_aux.loc[0,"city"]
        registro = df_aux.loc[0,"restaurant_id"]

        st.markdown("<h3 style='text-align: center;'>Cidade que possui mais restaurantes registrados</h3>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Cidade:</strong> {nome}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Restaurantes registrados:</strong> {registro}</p>", unsafe_allow_html=True)
        

        
        #Qual o nome da cidade que possui o maior valor médio de um prato para dois?
        df_aux = for_two_city(df1)
        nome = df_aux.loc[0,"city"]
        valor = df_aux.loc[0,"average_cost_for_two"]

        st.markdown("<h3 style='text-align: center;'>Possui o maior valor médio de um prato para dois</h3>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Cidade:</strong> {nome}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Valor:</strong> {valor}</p>", unsafe_allow_html=True)



        #Qual o nome da cidade que possui a maior quantidade de tipos de culinária distintas?
        df_aux = cuisines_distinct(df1)
        nome = df_aux.loc[0,"city"]
        culinarias = df_aux.loc[0,"cuisines"]

        st.markdown("<h3 style='text-align: center;'>Possui a maior quantidade de tipos de culinária distintas</h3>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Cidade:</strong> {nome}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Quantidades de culinárias distintas:</strong> {culinarias}</p>", unsafe_allow_html=True)



with tab2:
    with st.container():
        st.header("Restaurantes com nota média acima de 4")
        #Qual o nome da cidade que possui mais restaurantes com nota média acima de 4?        
        fig = avg_4(df1)
        st.plotly_chart(fig,use_container_width=True)

        
        st.markdown("""---""")

        
        #Qual o nome da cidade que possui mais restaurantes com nota média abaixo de 2.5?
        st.header("Restaurantes com nota média abaixo de 2.5")
        fig = avg_2_5(df1)
        st.plotly_chart(fig,use_container_width=True)


        
with tab3:
    with st.container():
        col1,col2 = st.columns(2)

        with col1:
            #Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem reservas?
            df_aux = table_or_delivering(df1,"table")
            nome = df_aux.loc[0,"city"]
            quantidade = df_aux.loc[0,"restaurant_id"]

            st.markdown("<h3 style='text-align: center;'>Possui a maior quantidade de restaurantes que fazem reservas</h3>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Cidade:</strong> {nome}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Restaurantes:</strong> {quantidade}</p>", unsafe_allow_html=True)


        
        with col2:
            #Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem entregas?
            df_aux = table_or_delivering(df1,"delivering")
            nome = df_aux.loc[0,"city"]
            quantidade = df_aux.loc[0,"restaurant_id"]

            st.markdown("<h3 style='text-align: center;'>Possui a maior quantidade de restaurantes que fazem entregas</h3>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Cidade:</strong> {nome}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Restaurantes:</strong> {quantidade}</p>", unsafe_allow_html=True)

    
    
    with st.container():
        st.markdown("""---""")
        #Qual o nome da cidade que possui a maior quantidade de restaurantes que aceitam pedidos online?
        df_aux = delivery_city(df1)    
        nome = df_aux.loc[0,"city"]
        quantidade = df_aux.loc[0,"restaurant_id"]

        st.markdown("<h3 style='text-align: center;'>Possui a maior quantidade de restaurantes que aceitam pedidos online</h3>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Cidade:</strong> {nome}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Restaurantes:</strong> {quantidade}</p>", unsafe_allow_html=True)
