#============================ PROJETO ALUNO ====================================#

#Importação das Bibliotecas

import pandas as pd
import numpy as np
import inflection
import streamlit as st
import plotly.express as px

#Importação do dataset
df = pd.read_csv('zomato.csv')

st.set_page_config(page_title="Visão Culinária",page_icon="🍔")

#========================== TRATAMENTO DOS DADOS ===============================#


#Cópia do dataframe
df1 = df.copy()

#Excluir as linhas com valores vazios 
df1 = df1.dropna()


#===================================== FUNÇÕES =================================#

def culinaria(df1,x,y):

    '''Passamos um dataframe para a função a qual retorna um novo organizado por tipo
    de culinária em ordem crescente ou decrescente, precisamos passar como parâmetros
    exatamente o tipo de culinária que esteja contido no conjunto de dados e indicar
    se queremos a maior média de avaliações ou a menor.'''
    
    if y=="maior":
        df_aux = (df1.loc[df1["cuisines"]==x,["restaurant_id","restaurant_name","aggregate_rating"]]
                     .groupby(["restaurant_id","restaurant_name"])
                     .mean()
                     .sort_values(["aggregate_rating","restaurant_id"],ascending=[False,True])
                     .reset_index())
                    
    if y=="menor":
        df_aux = (df1.loc[df1["cuisines"]==x,["restaurant_id","restaurant_name","aggregate_rating"]]
                     .groupby(["restaurant_id","restaurant_name"])
                     .mean()
                     .sort_values(["aggregate_rating","restaurant_id"],ascending=[True,True])
                     .reset_index())
    else:
        print("Erro")
        
    return df_aux  



def cusines_best_average(df1):
    #Me retorna um gráfico com as 15 culinárias com a melhor média
    df_1 = (df1.loc[:,["cuisines","aggregate_rating"]]
               .groupby(["cuisines"])
               .mean()
               .sort_values("aggregate_rating",ascending=False)
               .reset_index())
        
    df_aux = df_1.loc[0:15,:]
            
    fig = px.line(df_aux,x="cuisines",y="aggregate_rating")
    return fig 

    

def for_two_avg(df1):
    #Me retorna um dataframe com o maior valor médio de um prato para duas pessoas
            
    df_aux = (df1.loc[:,["cuisines","average_cost_for_two"]]
                 .groupby(["cuisines"])
                 .max()
                 .sort_values("average_cost_for_two",ascending=False)
                 .reset_index())
    
    return df_aux



def delivery_cuisines(df1):
    #Me retorna um dataframe com o tipo de culinaria que aceita pedidos online e faz entrega
    df_aux = (df1.loc[(df1["has_online_delivery"]==1)&(df1["is_delivering_now"]==1),["cuisines","restaurant_id"]]
                 .groupby(["cuisines"])
                 .count()
                 .sort_values("restaurant_id",ascending=False)
                 .reset_index())
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
country_options = st.sidebar.multiselect("Selecione os países os quais deseja obter informções:",["United States of America","England","United Arab Emirates","Brazil","India","Canada","Turkey"],default=["United States of America","England","United Arab Emirates","Brazil","India","Canada","Turkey"])

   
# A função isin() é usada para filtrar dados em um DataFrame ou Series com base em uma lista de valores. Ela retorna uma máscara booleana indicando quais elementos estão presentes na lista fornecida.
    
linhas_selecionadas = df1["country_code"].isin(numero_paises(country_options))
df1 = df1.loc[linhas_selecionadas,:]



#Filtro slider

range = st.sidebar.slider("Faixa de preço dos restaurantes:", min_value=1, max_value=4, value=4)

linhas_selecionadas = df1["price_range"]<=range
df1 = df1.loc[linhas_selecionadas,:]


#============================ VISÃO CULINARIA ====================================#

st.header("🍔Visão Culinária")

tab1,tab2 = st.tabs(["Geral","Métricas"])

with tab1:
    with st.container():
        st.header("Italian:")
        col1,col2 = st.columns(2)

        
        with col1:
            #Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a maior média de avaliação?      
            df_aux = culinaria(df1,"Italian","maior")
            nome = df_aux.loc[0,"restaurant_name"]
            avaliacao = df_aux.loc[0,"aggregate_rating"]

            st.markdown("<h3 style='text-align: center;'>Maior média de avaliação</h3>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Restaurante:</strong> {nome}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Avaliações:</strong> {avaliacao}</p>", unsafe_allow_html=True)


        
        with col2:
            #Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a menor média de avaliação?
            df_aux = culinaria(df1,"Italian","menor")
            nome = df_aux.loc[0,"restaurant_name"]
            avaliacao = df_aux.loc[0,"aggregate_rating"]
        
            st.markdown("<h3 style='text-align: center;'>Menor média de avaliação</h3>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Restaurante:</strong> {nome}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Avaliações:</strong> {avaliacao}</p>", unsafe_allow_html=True)


    
    with st.container():
        st.markdown("""---""")
        st.header("American:")
        col1,col2 = st.columns(2)
    
        with col1:
            #Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a maior média de avaliação?
            df_aux = culinaria(df1,"American","maior")
            nome = df_aux.loc[0,"restaurant_name"]
            avaliacao = df_aux.loc[0,"aggregate_rating"]
    
            st.markdown("<h3 style='text-align: center;'>Maior média de avaliação</h3>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Restaurante:</strong> {nome}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Avaliações:</strong> {avaliacao}</p>", unsafe_allow_html=True)
    

        
        with col2:
            #Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a menor média de avaliação?
            df_aux = culinaria(df1,"American","menor")
            nome = df_aux.loc[0,"restaurant_name"]
            avaliacao = df_aux.loc[0,"aggregate_rating"]
    
            st.markdown("<h3 style='text-align: center;'>Menor média de avaliação</h3>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Restaurante:</strong> {nome}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Avaliações:</strong> {avaliacao}</p>", unsafe_allow_html=True)
    
    
    with st.container():
        st.markdown("""---""")
        st.header("Arabian:")
        col1,col2 = st.columns(2)
    
        with col1:
            #Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a maior média de avaliação?
            df_aux = culinaria(df1,"Arabian","maior")
            nome = df_aux.loc[0,"restaurant_name"]
            avaliacao = df_aux.loc[0,"aggregate_rating"]
    
            st.markdown("<h3 style='text-align: center;'>Maior média de avaliação</h3>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Restaurante:</strong> {nome}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Avaliações:</strong> {avaliacao}</p>", unsafe_allow_html=True)
    

        
        with col2:
            #Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a menor média de avaliação?
            df_aux = culinaria(df1,"Arabian","menor")
            nome = df_aux.loc[0,"restaurant_name"]
            avaliacao = df_aux.loc[0,"aggregate_rating"]
    
            st.markdown("<h3 style='text-align: center;'>Menor média de avaliação</h3>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Restaurante:</strong> {nome}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Avaliações:</strong> {avaliacao}</p>", unsafe_allow_html=True)
        

    
    with st.container():
        st.markdown("""---""")
        st.header("Japanese:")
        col1,col2 = st.columns(2)
    
        with col1:
            #Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a maior média de avaliação?
            df_aux = culinaria(df1,"Japanese","maior")
        
            nome = df_aux.loc[0,"restaurant_name"]
            avaliacao = df_aux.loc[0,"aggregate_rating"]
    
            st.markdown("<h3 style='text-align: center;'>Maior média de avaliação</h3>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Restaurante:</strong> {nome}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Avaliações:</strong> {avaliacao}</p>", unsafe_allow_html=True)


        
        with col2:
            #Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a menor média de avaliação?
            df_aux = culinaria(df1,"Japanese","menor")
            nome = df_aux.loc[0,"restaurant_name"]
            avaliacao = df_aux.loc[0,"aggregate_rating"]
    
            st.markdown("<h3 style='text-align: center;'>Menor média de avaliação</h3>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Restaurante:</strong> {nome}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Avaliações:</strong> {avaliacao}</p>", unsafe_allow_html=True)    
        
    with st.container():
        st.markdown("""---""")
        st.header("Home-made:")
        col1,col2 = st.columns(2)
    
        with col1:
            #Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a maior média de avaliação?
            df_aux = culinaria(df1,"Home-made","maior")
            nome = df_aux.loc[0,"restaurant_name"]
            avaliacao = df_aux.loc[0,"aggregate_rating"]
    
            st.markdown("<h3 style='text-align: center;'>Maior média de avaliação</h3>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Restaurante:</strong> {nome}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Avaliações:</strong> {avaliacao}</p>", unsafe_allow_html=True)
    

        
        with col2:
            #Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a menor média de avaliação?
            df_aux = culinaria(df1,"Home-made","menor")
            nome = df_aux.loc[0,"restaurant_name"]
            avaliacao = df_aux.loc[0,"aggregate_rating"]
    
            st.markdown("<h3 style='text-align: center;'>Menor média de avaliação</h3>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Restaurante:</strong> {nome}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Avaliações:</strong> {avaliacao}</p>", unsafe_allow_html=True)



with tab2:
    with st.container():
        #Qual o tipo de culinária que possui a maior nota média?
        st.header("Culinárias com a maior nota média")
        fig = cusines_best_average(df1)
        st.plotly_chart(fig,use_container_width=True)

        
        
        st.markdown("""---""")
        #Qual o tipo de culinária que possui o maior valor médio de um prato para duas pessoas?
        df_aux = for_two_avg(df1)
        nome = df_aux.loc[0,"cuisines"]
        custo = df_aux.loc[0,"average_cost_for_two"]
    
        st.markdown("<h3 style='text-align: center;'>Culinária que possui o maior valor médio de um prato para duas pessoas</h3>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Culinária:</strong> {nome}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Valor médio:</strong> {custo}</p>", unsafe_allow_html=True)
    
    

        st.markdown("""---""")
        #Qual o tipo de culinária que possui mais restaurantes que aceitam pedidos online e fazem entregas?
        df_aux = delivery_cuisines(df1)
        nome = df_aux.loc[0,"cuisines"]
    
        st.markdown("<h3 style='text-align: center;'>Culinária que possui mais restaurantes que aceitam pedidos online e fazem entregas</h3>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Culinária:</strong> {nome}</p>", unsafe_allow_html=True)