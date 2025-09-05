import streamlit as st
import pandas as pd
from utils.sheets import get_worksheet

def mostrar_pagina():
    st.title("Gestão de Turmas")

    sheet = get_worksheet("Turmas")

    st.subheader("Adicionar turma")
    with st.form("form_turma"):
        nome_turma = st.text_input("Nome da turma")
        sala = st.text_input("Sala")
        submit = st.form_submit_button("Guardar")

    if submit:
        if nome_turma.strip() == "" or sala.strip() == "":
            st.error("Por favor, preencha todos os campos antes de guardar.")
        else:
            sheet.append_row([nome_turma, sala])
            st.success(f"Turma '{nome_turma}' na sala '{sala}' adicionada ao Google Sheets!")

    st.divider()
    st.subheader("Lista de turmas")

    dados = sheet.get_all_records()

    if dados:
        df = pd.DataFrame(dados)
        pesquisa = st.text_input("Pesquisar turma por nome ou sala:")

        if pesquisa:
            df_filtrado = df[df.apply(lambda row: pesquisa.lower() in row.astype(str).str.lower().to_string(), axis=1)]
        else:
            df_filtrado = df

        st.dataframe(df_filtrado, use_container_width=True)
    else:
        st.info("Ainda não existem turmas registadas.")

