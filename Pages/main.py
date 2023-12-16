import streamlit as st
from qualidade import quality
from home import home
from nocivos import nocivo

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

paginas = st.sidebar.selectbox("Escolha uma página", ("Home", "Qualidade: ar e água", "Agentes"))

if paginas == "Home":
    home()

if paginas == "Qualidade: ar e água":
    quality()

if paginas == "Agentes":
    nocivo()