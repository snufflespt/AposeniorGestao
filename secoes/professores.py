import streamlit as st
import pandas as pd
from utils.sheets import get_worksheet

def mostrar_pagina():
    st.title("Gestão de Professores")

    # Ligar à folha "Professores"
    sheet = get_worksheet("Professores")

    # Formulário para adicionar professor
    st.subheader("Adicionar professor")
    with st.form("form_professor"):
        nome_prof = st.text_input("Nome do professor")
        disciplina = st.text_input("Disciplina")
        submit = st.form_submit_button("Guardar")

    if submit:
        if nome_prof.strip() == "" or disciplina.strip() == "":
            st.error("Por favor, preencha todos os campos antes de guardar.")
        else:
            sheet.append_row([nome_prof, disciplina])
            st.success(f"Professor '{nome_prof}' de '{disciplina}' adicionado ao Google Sheets!")

    st.divider()
    st.subheader("Lista de professores")

    # Ler dados
    dados = sheet.get_all_records()

    if dados:
        df = pd.DataFrame(dados)

        # Pesquisa
        pesquisa = st.text_input("Pesquisar professor por nome ou disciplina:")
        if pesquisa:
            df_filtrado = df[df.apply(lambda row: pesquisa.lower() in row.astype(str).str.lower().to_string(), axis=1)]
        else:
            df_filtrado = df

        # Listagem com botões
        for i, row in df_filtrado.iterrows():
            col1, col2, col3 = st.columns([3, 2, 2])
            col1.write(f"**{row['Nome do Professor']}** — {row['Disciplina']}")
            if col2.button("✏️ Editar", key=f"edit_prof_{i}"):
                st.session_state['edit_prof_index'] = i
            if col3.button("🗑️ Apagar", key=f"delete_prof_{i}"):
                st.session_state['delete_prof_index'] = i

        # Confirmação de apagar
        if 'delete_prof_index' in st.session_state:
            idx = st.session_state['delete_prof_index']
            st.warning(f"Tens a certeza que queres apagar o professor: {df.iloc[idx]['Nome do Professor']}?")
            col_conf1, col_conf2 = st.columns(2)
            if col_conf1.button("✅ Sim, apagar"):
                sheet.delete_rows(idx+2)
                del st.session_state['delete_prof_index']
                st.rerun()
            if col_conf2.button("❌ Cancelar"):
                del st.session_state['delete_prof_index']
                st.rerun()

        # Edição
        if 'edit_prof_index' in st.session_state:
            idx = st.session_state['edit_prof_index']
            st.subheader("Editar professor")
            with st.form("form_editar_prof"):
                novo_nome = st.text_input("Nome do professor", value=df.iloc[idx]['Nome do Professor'])
                nova_disciplina = st.text_input("Disciplina", value=df.iloc[idx]['Disciplina'])
                guardar = st.form_submit_button("Guardar alterações")
            if guardar:
                sheet.update_cell(idx+2, 1, novo_nome)  # Coluna 1 = Nome do Professor
                sheet.update_cell(idx+2, 2, nova_disciplina)  # Coluna 2 = Disciplina
                del st.session_state['edit_prof_index']
                st.rerun()

    else:
        st.info("Ainda não existem professores registados.")
