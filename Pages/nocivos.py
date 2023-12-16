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
    fig.update_layout(xaxis_title="Substância", yaxis_title="Resultado", legend_title="Grupo", paper_bgcolor="skyblue")
    st.plotly_chart(fig)

def nocivo():
    st.title("Análise de Substâncias Encontradas na Água")

    df2 = carregar_dados()

    efeitos_saude = {'2, 4, 6 Triclorofenol': 'Efeitos dermatológicos, gastrointestinais e neurológicos',
        'Trihalometanos Total': 'Possíveis efeitos na saúde após consumo a longo prazo',
        'Ácidos haloacéticos total': 'Possíveis efeitos na saúde após consumo a longo prazo',
        'Nitrato (como N)': 'Risco de metahemoglobinemia em bebês',
        'Terbufós': 'Neurotoxicidade, irritação ocular e respiratória',
        'Cloreto de Vinila': 'Câncer de fígado',
        'Bário': 'Irritação gastrointestinal, muscular e cardiovascular',
        'Chumbo': 'Neurotoxicidade, afeta o desenvolvimento cerebral',
        'Cádmio': 'Problemas renais e pulmonares',
        'Mercúrio': 'Danos ao sistema nervoso central',
        'Tetracloreto de Carbono': 'Problemas hepáticos e renais',
        'Clordano': 'Possível carcinogênese, problemas neurológicos',
        'Antimônio': 'Irritação gastrointestinal e pulmonar',
        'Endrin': 'Neurotoxicidade',
        'Metamidofós': 'Neurotoxicidade, problemas respiratórios',
        'Metolacloro': 'Irritação ocular e respiratória',
        'Arsênio': 'Câncer, problemas cardíacos e respiratórios',
        'Pendimetalina': 'Irritação ocular, cutânea e pulmonar',
        '1,2 Dicloroeteno (cis + trans)': 'Irritação ocular, cutânea e pulmonar',
        'Cobre': 'Problemas gastrointestinais, hepáticos e renais',
        'Níquel': 'Possível carcinogênese, problemas pulmonares',
        'Permetrina': 'Irritação cutânea e ocular',
        'Benzo[a]pireno': 'Carcinogênese',
        'Acrilamida': 'Possível carcinogênese, problemas nervosos',
        'Lindano (gama HCH)': 'Neurotoxicidade, possíveis danos hepáticos',
        'DDT + DDD + DDE': 'Possível carcinogênese, problemas endócrinos',
        'Cromo': 'Irritação pulmonar e nasal, problemas renais',
        'Aldrin + Dieldrin': 'Possível carcinogênese, problemas neurológicos',
        'Urânio': 'Problemas renais, danos ao sistema nervoso',
        'Selênio': 'Problemas gastrointestinais, respiratórios e neurológicos',
        'Diclorometano': 'Possível carcinogênese, problemas hepáticos',
        'Carbofurano': 'Neurotoxicidade, problemas respiratórios',
        'Nitrito (como N)': 'Risco de metahemoglobinemia em bebês',
        'Simazina': 'Irritação ocular e cutânea, problemas gastrointestinais',
        'Trifluralina': 'Irritação ocular, cutânea e pulmonar',
        'Parationa Metílica': 'Neurotoxicidade, problemas respiratórios',
        '1,1 Dicloroeteno': 'Irritação ocular, cutânea e pulmonar',
        'Cianeto': 'Toxicidade sistêmica, afeta o sistema nervoso',
        'Rádio-228': 'Possível carcinogênese, problemas ósseos',
        'Atividade alfa total': 'Possível carcinogênese, danos às células',
        'Benzeno': 'Carcinogênese, problemas hematológicos',
        '1,2 Dicloroetano': 'Irritação ocular, cutânea e pulmonar',
        'Triclorobenzenos': 'Irritação ocular, cutânea e pulmonar',
        'Glifosato + AMPA': 'cancerígeno',
        'Aldicarbe + Aldicarbesulfona + Aldicarbesulfóxido': 'Neurotoxicidade, problemas respiratórios',
        'Di (2-etilhexil) ftalato': 'Possíveis efeitos adversos à saúde humana',
        'Atrazina': 'Possíveis efeitos adversos à saúde humana',
        'Tetracloroeteno': 'Possível carcinogênese, problemas hepáticos e renais',
        'Diuron': 'Possíveis efeitos adversos à saúde humana',
        'Clorpirifós + clorpirifós-oxon': 'Neurotoxicidade, problemas respiratórios',
        'Estireno': 'Irritação ocular, cutânea e pulmonar',
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

    st.markdown("""Fonte dos dados  
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


