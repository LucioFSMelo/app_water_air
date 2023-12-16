import pandas as pd
import streamlit as st
import plotly.express as px

def carregar_dados():
    url = 'Datasets/substancias_quimicas.csv'
    return pd.read_csv(url)

def criar_grafico_rosca(data, nome_col1, nome_col2, cidade):
    fig = px.line_polar(
        data,
        r=nome_col1,
        theta=nome_col2,
        line_close=True,
        title=f"Resultados de Substâncias em {cidade}",
        height=400
    )
    fig.update_layout(polar=dict(radialaxis=dict(title="Resultado")))
    st.plotly_chart(fig)

def criar_grafico_barras(data, cidade):
    fig = px.bar(
        data,
        x="substancia",
        y="resultado",
        color="grupo",
        title=f"Resultados de Substâncias em {cidade}",
        labels={"resultado": "Resultado", "substancia": "Substância"},
        height=400,
        barmode="stack"
    )
    fig.update_layout(xaxis_title="Substância", yaxis_title="Resultado", legend_title="Grupo")
    st.plotly_chart(fig)

def nocivo():
    st.title("Análise de Substâncias Encontradas na Água")

    df2 = carregar_dados()

    efeitos_saude = {'2, 4, 6 Triclorofenol': 'Efeitos dermatológicos, gastrointestinais e neurológicos',
        # ... (restante do dicionário) ...
        'Profenofós': 'Neurotoxicidade, problemas respiratórios'}

    df2['efeitos_saude'] = df2['substancia'].map(efeitos_saude)

    escolha_regiao = st.sidebar.selectbox("Selecione a Região", df2["regiao_geografica"].unique())
    ufs_regiao = df2[df2["regiao_geografica"] == escolha_regiao]["uf"].unique()
    escola_uf = st.sidebar.selectbox("Selecione a UF", ufs_regiao)
    cidade_regiao_uf = df2[(df2["regiao_geografica"] == escolha_regiao) & (df2["uf"] == escola_uf)]["municipio"].unique()
    escolha_cidade = st.sidebar.selectbox("Selecione a Cidade", cidade_regiao_uf)

    filtered_df = df2[(df2["regiao_geografica"] == escolha_regiao) & (df2["uf"] == escola_uf) & (df2["municipio"] == escolha_cidade)]

    st.subheader(f"Substâncias em {escolha_cidade}, {escola_uf} - {escolha_regiao}")
    st.table(filtered_df[["substancia", "pt_monitoramento", "grupo", "efeitos_saude"]])

    criar_grafico_barras(filtered_df, escolha_cidade)
    # criar_grafico_rosca(filtered_df, 'substancia', 'resultado', escolha_cidade)

    st.markdown("""Fonte do dados  
                Metodologia do Mapa da Água: https://mapadaagua.reporterbrasil.org.br/metodologia  
                * VMP (Valor Máximo Permitido): concentração máxima permitida para cada substância na água.  
                Este valor é determinado pelo Ministério da Saúde.  
                * Resultado: concentração da substância testada. Quando não quantificado, pode ser expresso  
                como "menor que LD" ou "menor que LQ".  
                * LD (Limite de Detecção): valor mínimo que o equipamento consegue captar a presença de certa  
                substância na água. Segundo o Ministério da Saúde, “ Menor que LD” significa que a substância  
                está ausente daquela amostra de água ou em concentração inferior àquela que o equipamento  
                consegue detectar.  
                * LQ (Limite de Quantificação): valor mínimo que o equipamento consegue medir a concentração  
                de certa substância na água. Segundo o Ministério da Saúde, “Menor que LQ” é quando é possível  
                identificar a presença daquela substância na água, mas não a concentração existente.  
                * Tipo_cor 1: são as “substâncias com os maiores riscos de gerar doenças crônicas, como câncer”  
                * Tipo_cor 2: são as outras “substâncias que geram riscos à saúde”  
                Dicionário de dados do Sisagua / Ministério da Saúde:  
                https://dados.gov.br/dataset/controle-semestral/resource/7f74253a-2cdd-411f-9d96-8e88a5638d85""")

if __name__=='__main__':
    nocivo()


