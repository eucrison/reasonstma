# ===============================================
# requests.py
# ===============================================
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

# ==============================
# Função principal de leitura
# ==============================
def load_data(uploaded_file):
    df = pd.read_csv(uploaded_file)
    df.columns = [c.strip().lower() for c in df.columns]
    return df

# ==============================
# Análises estatísticas
# ==============================
def resumo_geral(df):
    resumo = {
        "Total de registros": len(df),
        "Total de agentes únicos": df["agente_email"].nunique(),
        "Total de líderes únicos": df["lider"].nunique() if "lider" in df.columns else None,
        "Tempo médio geral (s)": df["tma_segundos"].mean(),
        "Tempo máximo (s)": df["tma_segundos"].max(),
        "Tempo mínimo (s)": df["tma_segundos"].min(),
        "Média de tickets por agente": df.groupby("agente_email")["qtd_motivos"].sum().mean(),
    }
    return resumo

# ==============================
# Tabelas de ranking
# ==============================
def top_agentes_qtd(df, n=10):
    return (
        df.groupby("agente_email")["qtd_motivos"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
        .reset_index()
    )

def top_agentes_tma(df, n=10):
    media_tma = df.groupby("agente_email")["tma_segundos"].mean().reset_index()
    return (
        media_tma.sort_values("tma_segundos")
        .head(n)
        .rename(columns={"tma_segundos": "tma_medio"})
    ), (
        media_tma.sort_values("tma_segundos", ascending=False)
        .head(n)
        .rename(columns={"tma_segundos": "tma_medio"})
    )

# ==============================
# Gráficos
# ==============================
def grafico_boxplot_tma(df):
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.boxplot(x=df["tma_segundos"], color="#9ecae1", ax=ax, showfliers=False)
    ax.set_title("Distribuição do Tempo Médio de Atendimento (TMA)")
    ax.set_xlabel("Tempo (segundos)")
    return fig

def grafico_dispersa_produtividade(df):
    df_agente = df.groupby("agente_email").agg(
        qtd_total=("qtd_motivos", "sum"),
        tma_medio=("tma_segundos", "mean")
    ).reset_index()

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(
        data=df_agente,
        x="qtd_total",
        y="tma_medio",
        alpha=0.7,
        ax=ax,
        color="#3182bd"
    )
    ax.set_title("Relação entre Volume de Tickets e TMA por Agente")
    ax.set_xlabel("Volume de tickets")
    ax.set_ylabel("TMA médio (segundos)")
    return fig

def grafico_barra_media(df, coluna, titulo):
    df_media = df.groupby(coluna)["tma_segundos"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(8, 5))
    df_media.plot(kind="barh", ax=ax, color="#6baed6")
    ax.set_title(f"TMA médio por {coluna.capitalize()}")
    ax.set_xlabel("TMA médio (segundos)")
    ax.grid(axis="x", linestyle="--", alpha=0.6)
    return fig
