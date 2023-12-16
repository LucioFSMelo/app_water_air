import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import altair as alt

# Função para leitura do dataframe
@st.cache_data
def load_data(url):
    df = pd.read_csv(url, header = 0,
    names = ['cidade', 'regiao', 'pais', 'qualidade_ar', 'poluicao_agua']) 
    return df


df1 = load_data(df1 = load_data('Datasets/cities_air_quality_water_pollution.18-10-2021 (1).csv'))

# Retirando as aspas com a função strip()
df1['pais'] = df1['pais'].str.strip(' ""')
df1['regiao'] = df1['regiao'].str.strip(' ""')

# Filtrando o dataframe para trabalhar apenas com o brasil
df_brasil = df1.query('pais == "Brazil"')

# Função para o gráfico de barras
def graf_barras(data, nome_col1, nome_col2, estado):
    # Criar gráfico de poluição da água por cidade
    fig = px.bar(
        data,    #df_regiao
        x=nome_col1,   #coluna - cidade
        y=nome_col2,   # coluna - poluicao_agua
        title=f"Poluição da Água por Cidade em {estado}",        #seleciona_estado
        labels={"poluicao_agua": "Nível de Poluição da Água", "cidade": "Cidade"},
        color=nome_col2,
        color_continuous_scale="viridis"
    )

    # Personalizar layout do gráfico
    fig.update_layout(
        xaxis_title="Cidade",
        yaxis_title="Nível de Poluição da Água",
        coloraxis_colorbar_title="Nível de Poluição da Água",
        barmode="group",
        paper_bgcolor="skyblue"
    )

    # Exibindo o gráfico
    graf_region = st.sidebar.button("Gráfico da Região")
    if graf_region:
        return st.plotly_chart(fig)


# Função para gerar o segundo gráfico, aqui vamos passas novamente o df_region
def graf_scater(data):
    # Escaterplot
    Xa = "qualidade_ar"
    Ya = "poluicao_agua"

    fig2 = px.scatter(data, x=Xa, y=Ya, text="cidade", color="pais", size_max=100)

    # Personalizar o layout do gráfico
    fig2.update_layout(
        title="Diferenças na Qualidade do Ar e Poluição da Água entre Cidades",
        xaxis_title="Qualidade do Ar",
        yaxis_title="Poluição da Água",
        hovermode="closest",
        paper_bgcolor="skyblue"
    )

    # Exibir o gráfico
    st.sidebar.markdown('**Diferenças entre as Cidades**')
    graf_Scatter = st.sidebar.button("Água vs Ar")
    if graf_Scatter:
        return st.plotly_chart(fig2)
    
# Função para criar o gráfico de velocímetro

# Função para criar o gráfico de velocímetro
def create_gauge_chart(value, max_value, title):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title}
    ))

    fig.update_layout(
        width=240,
        height=150,
        margin=dict(l=20, r=20, b=20, t=20),
        paper_bgcolor="skyblue"
    )

    return fig

def quality():
    # Iniciando a aplicação Streamlit
    st.title("BRASIL - Qualidade da Água e do Ar")
    st.text("A qualidade do ar varia de 0 (má qualidade) a 100 (melhor qualidade)")
    st.text('A poluição da água varia de 0 (sem poluição) a 100 (poluição extrema)')

    # Filtrar por Estado
    seleciona_estado = st.sidebar.selectbox("Selecione o Estado", df_brasil["regiao"].unique())

    # Filtrar por Cidade
    cidades_por_estado = df_brasil[df_brasil["regiao"] == seleciona_estado]["cidade"].unique()
    seleciona_cidades = st.sidebar.selectbox("Selecione a Cidade", cidades_por_estado)

    # Exibir dados de qualidade do ar e poluição da água
    seleciona_dados = df_brasil[(df_brasil["regiao"] == seleciona_estado) & (df_brasil["cidade"] == seleciona_cidades)]

    st.subheader(f"Dados para {seleciona_cidades}, {seleciona_estado}")
    #st.write(f"Qualidade do Ar: {seleciona_dados['qualidade_ar'].values[0]}")
    #st.write(f"Poluição da Água: {seleciona_dados['poluicao_agua'].values[0]}")

    # Criação dos gráficos de velocímetro
    st.subheader("Qualidade do Ar vs. Poluição da Água")

    # Configuração dos widgets de coluna
    col1, col2 = st.columns(2)

    with col1:
        st.write("## Qualidade do Ar")
        st.plotly_chart(create_gauge_chart(seleciona_dados['qualidade_ar'].values[0], 100, "Qualidade do Ar"))

    with col2:
        st.write("## Poluição da Água")
        st.plotly_chart(create_gauge_chart(seleciona_dados['poluicao_agua'].values[0], 100, "Poluição da Água"))

    #Filtrando um gráfico por região
    df_region = df_brasil[df_brasil["regiao"] == seleciona_estado]

    # Passando o primero gráfico
    graf_barras(df_region, 'cidade', 'poluicao_agua', seleciona_estado)

    #Passando o segundo gráfico
    graf_scater(df_region)




if __name__=="__main__":
    quality()