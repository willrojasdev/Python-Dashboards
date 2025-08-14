import streamlit as st
import pandas as pd

tabela = pd.read_excel(r"C:\Users\William Rojas\Documents\Dashboard Python\Hashtag\Montagem - AppSheet.xlsx")

# Título
st.title("Dashboard de produção - Montagem")

# Campo de seleção e filtro dos dados
data = st.multiselect("Selecione a data", tabela["data"].unique())

if data:
    tabela = tabela[tabela["data"].isin(data)]

# Métricas
# Produção em peças
st.metric("Peças Produzidas", f"{tabela["id"].count()}")

# Produção em metros quadrados
st.metric("Metros quadrados Produzidos", f"{tabela["metro_quadrado"].sum()}")

# Gráfico de produção diária
st.bar_chart(tabela.groupby("data")["id"].count())

# Gráfico de veículos mais produzidos
st.bar_chart(tabela.groupby("descricao_carro")["id"].count())