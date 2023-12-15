import streamlit as st
from substancia import substancia_nociva
from qualidade import quality
from home import home

# Configuração da página
# Configuração da página
st.markdown(
    """
    <style>
        .main {
            background-color: #87CEEB; /* Azul céu */
            padding: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Conteúdo principal
st.markdown('<div class="main"></div>', unsafe_allow_html=True)


st.sidebar.title("MENU")

paginas = st.sidebar.selectbox("Escolha uma página", ("Home", "Qualidade: ar e água", "Substancias Nocivas a Saúde"))

if paginas == "Home":
    home()

if paginas == "Qualidade: ar e água":
    quality()

if paginas == "Substancias Nocivas a saúde":
    substancia_nociva()