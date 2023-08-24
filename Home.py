import streamlit as st
from PIL import Image

st.set_page_config(
    page_title = "Home",
    page_icon = "🏠",
    layout = "wide"
)

st.sidebar.header("Fome Zero Dashboard")

st.sidebar.write("O Melhor lugar para encontrar seu mais novo restaurante favorito!")

st.sidebar.markdown("""---""")



#Descrever como usar o dashboard
st.markdown("## Bem-vindo ao Fome Zero Dashboard! 👋")
st.write("Este painel foi projetado para fornecer uma visão abrangente dos dados disponíveis. "
         "Aqui estão as diferentes seções que você pode explorar:")

st.markdown("### Visão País:")
st.write("- **Geral:** Métricas gerais de comportamento.")
st.write("- **Qualificação:** Avaliações em geral dos países.")
st.write("- **Restaurante:** Métricas de restaurantes por países.")

st.markdown("### Visão Cidade:")
st.write("- **Geral:** Métricas gerais de comportamento.")
st.write("- **Métricas:** Visões relacionadas à nota média dos restaurantes por cidade.")
st.write("- **Serviços:** Entregas, reservas e delivery dos restaurantes por cidade.")

st.markdown("### Visão Restaurante:")
st.write("- **Geral:** Métricas gerais de comportamento.")
st.write("- **Visão a par:** Métricas de pratos para duas pessoas nos restaurantes.")

st.markdown("### Visão Culinária:")
st.write("- **Geral:** Métricas gerais de comportamento.")
st.write("- **Métricas:** Visões a respeito da nota média, valor médio e entregas por culinárias.")
