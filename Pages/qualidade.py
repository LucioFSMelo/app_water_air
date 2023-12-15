import pandas as pd
import streamlit as st
import plotly.express as px

# Função para leitura do dataframe
@st.cache_data
def load_data(url):
    df = pd.read_csv(url, header = 0,
    names = ['cidade', 'regiao', 'pais', 'qualidade_ar', 'poluicao_agua']) 
    return df


df1 = load_data('C:/Users/luciu/Workspace/Projeto_Qualidade/quality_water_air/Datasets/cities_air_quality_water_pollution.18-10-2021 (1).csv')

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
        barmode="group"
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
        hovermode="closest"
    )

    # Exibir o gráfico
    st.sidebar.markdown('**Diferenças entre as Cidades**')
    graf_Scatter = st.sidebar.button("Água vs Ar")
    if graf_Scatter:
        return st.plotly_chart(fig2)

def qualidade():
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
    st.write(f"Qualidade do Ar: {seleciona_dados['qualidade_ar'].values[0]}")
    st.write(f"Poluição da Água: {seleciona_dados['poluicao_agua'].values[0]}")


    #Filtrando um gráfico por região
    df_region = df_brasil[df_brasil["regiao"] == seleciona_estado]

    # Passando o primero gráfico
    graf_barras(df_region, 'cidade', 'poluicao_agua', seleciona_estado)

    #Passando o segundo gráfico
    graf_scater(df_region)




if __name__=="__main__":
    qualidade()