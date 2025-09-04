import streamlit as st
from pages import utentes  # Importa a página de utentes (e depois as outras)

st.set_page_config(page_title="Gestão IPSS", page_icon="🧭", layout="wide")

# Menu lateral
st.sidebar.title("Menu")
opcao = st.sidebar.radio("Escolhe a secção:", ["🏠 Início", "🧍 Utentes", "📚 Turmas", "👨‍🏫 Professores"])

# Mostrar a página escolhida
if opcao == "🏠 Início":
    st.title("Bem-vindo à Gestão IPSS")
    st.write("Usa o menu à esquerda para navegar entre as secções.")
elif opcao == "🧍 Utentes":
    utentes.mostrar_pagina()
elif opcao == "📚 Turmas":
    st.title("Gestão de Turmas")
    st.info("Página de turmas ainda por implementar.")
elif opcao == "👨‍🏫 Professores":
    st.title("Gestão de Professores")
    st.info("Página de professores ainda por implementar.")
