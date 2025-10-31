# ===============================================
# app.py
# ===============================================
import streamlit as st
import pandas as pd
import requests as rq

st.set_page_config(page_title="Análise de TMA e Tickets", layout="wide")

st.title("📊 Dashboard de Análise de Tickets e TMA")

st.write("""
Faça o upload de um arquivo `.csv` contendo as colunas:
`agente_email`, `lider`, `produto`, `Jornada`, `qtd_motivos`, `tma_segundos`.
""")

uploaded_file = st.file_uploader("Selecione o arquivo CSV", type=["csv"])

if uploaded_file:
    # Carrega e analisa os dados
    df = rq.load_data(uploaded_file)
    st.success(f"✅ Dados carregados com sucesso! Total de registros: {len(df)}")

    # ==========================
    # Resumo geral
    # ==========================
    st.header("📈 Resumo Geral")
    resumo = rq.resumo_geral(df)
    st.table(pd.DataFrame(resumo.items(), columns=["Indicador", "Valor"]))

    # ==========================
    # Rankings
    # ==========================
    st.header("🏅 Rankings de Agentes")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top 10 - Maior Volume de Tickets")
        st.dataframe(rq.top_agentes_qtd(df))

    with col2:
        st.subheader("Top 10 - Menor e Maior TMA Médio")
        menor, maior = rq.top_agentes_tma(df)
        st.write("**Menor TMA**")
        st.dataframe(menor)
        st.write("**Maior TMA**")
        st.dataframe(maior)

    # ==========================
    # Gráficos
    # ==========================
    st.header("📊 Visualizações")

    st.subheader("Distribuição Geral do TMA")
    st.pyplot(rq.grafico_boxplot_tma(df))

    st.subheader("Relação entre Produtividade e Tempo Médio")
    st.pyplot(rq.grafico_dispersa_produtividade(df))

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("TMA por Produto")
        st.pyplot(rq.grafico_barra_media(df, "produto", "Produto"))
    with col4:
        st.subheader("TMA por Jornada")
        st.pyplot(rq.grafico_barra_media(df, "Jornada", "Jornada"))

else:
    st.info("👆 Faça o upload de um arquivo CSV para iniciar a análise.")
