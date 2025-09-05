import streamlit as st
import pandas as pd
from utils.sheets import get_worksheet

def mostrar_pagina():
    st.title("Gestão de Turmas")

    # Ligar à folha "Turmas"
    sheet = get_worksheet("Turmas")

    # Formulário para adicionar turma
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

    # Ler dados
    dados = sheet.get_all_records()

    if dados:
        df = pd.DataFrame(dados)

        # Pesquisa
        pesquisa = st.text_input("Pesquisar turma por nome ou sala:")
        if pesquisa:
            df_filtrado = df[df.apply(lambda row: pesquisa.lower() in row.astype(str).str.lower().to_string(), axis=1)]
        else:
            df_filtrado = df

        # Listagem com botões
        for i, row in df_filtrado.iterrows():
            col1, col2, col3 = st.columns([3, 2, 2])
            col1.write(f"**{row['Nome da Turma']}** — Sala {row['Sala']}")
            if col2.button("✏️ Editar", key=f"edit_turma_{i}"):
                st.session_state['edit_turma_index'] = i
            if col3.button("🗑️ Apagar", key=f"delete_turma_{i}"):
                st.session_state['delete_turma_index'] = i

        # Confirmação de apagar
        if 'delete_turma_index' in st.session_state:
            idx = st.session_state['delete_turma_index']
            st.warning(f"Tens a certeza que queres apagar a turma: {df.iloc[idx]['Nome da Turma']}?")
            col_conf1, col_conf2 = st.columns(2)
            if col_conf1.button("✅ Sim, apagar"):
                sheet.delete_rows(idx+2)
                del st.session_state['delete_turma_index']
                st.rerun()
            if col_conf2.button("❌ Cancelar"):
                del st.session_state['delete_turma_index']
                st.rerun()

        # Edição
        if 'edit_turma_index' in st.session_state:
            idx = st.session_state['edit_turma_index']
            st.subheader("Editar turma")
            with st.form("form_editar_turma"):
                novo_nome = st.text_input("Nome da turma", value=df.iloc[idx]['Nome da Turma'])
                nova_sala = st.text_input("Sala", value=df.iloc[idx]['Sala'])
                guardar = st.form_submit_button("Guardar alterações")
            if guardar:
                sheet.update_cell(idx+2, 1, novo_nome)  # Coluna 1 = Nome da Turma
                sheet.update_cell(idx+2, 2, nova_sala)  # Coluna 2 = Sala
                del st.session_state['edit_turma_index']
                st.rerun()

    else:
        st.info("Ainda não existem turmas registadas.")
