#============================ PROJETO ALUNO ====================================#

#Importação das Bibliotecas

import pandas as pd
import numpy as np
import inflection
import streamlit as st
import plotly.express as px

#Importação do dataset
df = pd.read_csv('zomato.csv')

st.set_page_config(page_title="Visão País",page_icon="🌍")


#========================== TRATAMENTO DOS DADOS ===============================#


#Cópia do dataframe
df1 = df.copy()
#Excluir as linhas com valores vazios 
df1 = df1.dropna()


#===================================== FUNÇÕES =================================#

def country_city(df1):
    #Retorna um gráfico com a quantidade de cidades registradas por país
    df_aux = (df1.loc[:,["country_code","city"]]
                 .groupby("country_code")
                 .count().sort_values(["city"],ascending=False)
                 .reset_index())
            
    for i in range(len(df_aux)):
        df_aux.loc[i,"country_code"]= country_name(df_aux.loc[i,"country_code"])
        
    fig = px.bar(df_aux,x="country_code",y="city")
            
    return fig



def cuisines_distincts(df1):
    #Retorna um dataframe com a quantidade de culinárias distintasa por país
    df_aux = (df1.loc[:,["country_code","cuisines"]]
                 .groupby(["country_code"])
                 .nunique()
                 .sort_values(["cuisines"],ascending=False)
                 .reset_index())
    return df_aux

def country_for_two(df1):
    #Retorna um gráfico com a média de preço de prato para dois por país
    df_aux = (df1.loc[:,["country_code","average_cost_for_two"]]
                 .groupby(["country_code"])
                 .mean()
                 .reset_index())
        
    for i in range(len(df_aux)):
        nome = df_aux.loc[i,"country_code"]
        df_aux.loc[i,"country_code"] = country_name(nome)
    
    fig = px.bar(df_aux,x="country_code",y="average_cost_for_two")
    return fig


def country_votes(df1,x):
    '''Retorna um dataframe com a maior quantidade de avaliações ou a média de 
    avaliações por país, alterando o parâmetro para "quantidade" ou "media"'''
    if x=="quantidade":
        df_aux =(df1.loc[:,["country_code","votes"]]
                    .groupby(["country_code"])
                    .sum()
                    .sort_values(["votes"],ascending=False)
                    .reset_index())
    if x=="media":
        df_aux = (df1.loc[:,["country_code","votes"]]
                     .groupby(["country_code"])
                     .mean()
                     .sort_values("votes",ascending=False)
                     .reset_index())
    else:
        print("Erro")

    return df_aux


def country_rating(df1,x):
    '''Retorna um dataframe com a maior ou menor nota média registrada alterando
    os parâmetros do x para maior ou menor''' 

    if x=="maior":
        
        df_aux = (df1.loc[:,["country_code","aggregate_rating"]]
                     .groupby(["country_code"])
                     .mean()
                     .sort_values("aggregate_rating",ascending=False)
                     .reset_index())
    if x=="menor":
        df_aux = (df1.loc[:,["country_code","aggregate_rating"]]
                     .groupby(["country_code"])
                     .mean().sort_values("aggregate_rating",ascending=True)
                     .reset_index())
    else:
        print("Erro")

    return df_aux

def country_restaurant(df1):
    #Retorna um gráfico com a quantidade de restaurantes registrados por país
    df_aux = (df1.loc[:,["country_code","restaurant_name"]]
                 .groupby("country_code")
                 .count()
                 .sort_values(["restaurant_name"],ascending=False)
                 .reset_index())
                  
    for i in range(len(df_aux)):
        df_aux.loc[i,"country_code"]= country_name(df_aux.loc[i,"country_code"])
    
    
    fig = px.bar(df_aux,x="country_code",y="restaurant_name")

    return fig



def country_restaurant_4(df1):
    #Retorna um datafram em ordem de país que contém mais restaurantes com o nível de preço igual 4 registrados
    df_aux = (df1.loc[df1["price_range"]==4,["country_code","price_range"]]
                 .groupby("country_code")
                 .count()
                 .sort_values(["price_range"],ascending=False)
                 .reset_index())
    return df_aux


def country_delivering_or_table(df1,x):
    '''Retorna um dataframe a quantidade de restaurantes que fazem entrega ou que aceitam reservas
    por páis, passando como parâmetros delivering ou table'''
    if x=="delivering":
        df_aux = (df1.loc[df1["is_delivering_now"]==1,["country_code","is_delivering_now"]]
                     .groupby(["country_code"])
                     .count()
                     .sort_values(["is_delivering_now"],ascending=False)
                     .reset_index())

    if x=="table":
        df_aux = (df1.loc[df1["has_table_booking"]==1,["country_code","has_table_booking"]]
                     .groupby(["country_code"])
                     .count()
                     .sort_values("has_table_booking",ascending=False)
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



#============================ VISÃO PAÍSES ====================================#
st.header("🌍Visão País")

tab1,tab2,tab3 = st.tabs(["Geral","Qualificação","Restaurante"])


with tab1:
    with st.container():
        #Qual o nome do país que possui mais cidades registradas?
        st.header("Cidades registradas por países")
        fig = country_city(df1)
        st.plotly_chart(fig,use_container_width=True)


        
        #Qual o nome do país que possui a maior quantidade de tipos de culinária distintos?
        st.markdown("""---""")
        df_aux = cuisines_distincts(df1)
        nome = df_aux.loc[0,"country_code"]
        culinarias = df_aux.loc[0,"cuisines"]
    

        st.markdown("<h3 style='text-align: center;'>País que possui a maior quantidade de tipos de culinária distintos</h3>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Nome do País:</strong> {country_name(nome)}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Quantidade de culinárias distintas:</strong> {culinarias}</p>", unsafe_allow_html=True)


        
        # Qual a média de preço de um prato para dois por país?
        st.markdown("""---""")
        st.header("A média de preço de um prato para dois por país")
        fig = country_for_two(df1)
        st.plotly_chart(fig,use_container_width=True)



with tab2:
    with st.container():
        #Qual o nome do país que possui a maior quantidade de avaliações feitas?

        df_aux = country_votes(df1,"quantidade")
        nome = df_aux.loc[0,"country_code"]
        avaliacoes = df_aux.loc[0,"votes"]

        st.markdown("<h3 style='text-align: center;'>País que possui a maior quantidade de avaliações feitas</h3>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Nome do País:</strong> {country_name(nome)}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Avaliações feitas:</strong> {avaliacoes}</p>", unsafe_allow_html=True)


        
        #Qual o nome do país que possui, na média, a maior quantidade de avaliações registrada?

        df_aux = country_votes(df1,"media")       
        nome = df_aux.loc[0,"country_code"]
        avaliacao = df_aux.loc[0,"votes"]

        st.markdown("<h3 style='text-align: center;'>País que possui, na média, a maior quantidade de avaliações registrada</h3>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Nome do País:</strong> {country_name(nome)}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Avaliações registradas:</strong> {avaliacao}</p>", unsafe_allow_html=True)


        
        #Qual o nome do país que possui, na média, a maior nota média registrada?
        df_aux = country_rating(df1,"maior")
        nome = df_aux.loc[0,"country_code"]
        media = df_aux.loc[0,"aggregate_rating"]

        st.markdown("<h3 style='text-align: center;'>País que possui, na média, a maior nota média registrada</h3>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Nome do País:</strong> {country_name(nome)}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Nota média:</strong> {media}</p>", unsafe_allow_html=True)



        #Qual o nome do país que possui, na média, a menor nota média registrada?
        df_aux = country_rating(df1,"menor")
        nome = df_aux.loc[0,"country_code"]
        media = df_aux.loc[0,"aggregate_rating"]

        st.markdown("<h3 style='text-align: center;'>País que possui, na média, a menor quantidade de avaliações registrada</h3>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Nome do País:</strong> {country_name(nome)}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Nota média:</strong> {media}</p>", unsafe_allow_html=True)



with tab3:
    with st.container():
        
        #Qual o nome do país que possui mais restaurantes registrados?
        st.header("Restaurantes registrados por países")
        fig = country_restaurant(df1)
        st.plotly_chart(fig,use_container_width=True)

        
    
        #Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4 registrados?
        df_aux = country_restaurant_4(df1)
        nome = df_aux.loc[0,"country_code"]
        restaurantes = df_aux.loc[0,"price_range"]

        st.markdown("<h3 style='text-align: center;'>País que possui mais restaurantes com o nível de preço igual a 4</h3>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Nome do País:</strong> {country_name(nome)}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Quantidade de Resturantes:</strong> {restaurantes}</p>", unsafe_allow_html=True)


        
         #Qual o nome do país que possui a maior quantidade de restaurantes que fazem entrega?
        df_aux = country_delivering_or_table(df1,"delivering")
        nome = df_aux.loc[0,"country_code"]
        entrega = df_aux.loc[0,"is_delivering_now"]

        st.markdown("<h3 style='text-align: center;'>País que possui a maior quantidade de restaurantes que fazem entrega</h3>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Nome do País:</strong> {country_name(nome)}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Quantidade de restaurantes:</strong> {entrega}</p>", unsafe_allow_html=True)



        #Qual o nome do país que possui a maior quantidade de restaurantes que aceitam reservas?
        df_aux = country_delivering_or_table(df1,"table")
        nome = df_aux.loc[0,"country_code"]
        reservas = df_aux.loc[0,"has_table_booking"]
    
        st.markdown("<h3 style='text-align: center;'>País que possui a maior quantidade de restaurantes que aceitam reservas</h3>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Nome do País:</strong> {country_name(nome)}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Quantidade de reservas:</strong> {reservas}</p>", unsafe_allow_html=True)