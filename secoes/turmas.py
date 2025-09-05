import streamlit as st
import pandas as pd
from utils.sheets import get_worksheet

def mostrar_pagina():
    st.title("Gestão de Turmas")

    sheet_turmas = get_worksheet("Turmas")
    sheet_disc = get_worksheet("Disciplinas")

    # Obter lista de disciplinas
    disciplinas = sheet_disc.col_values(1)[1:]  # Ignora cabeçalho

    # Formulário para adicionar turma
    st.subheader("Adicionar turma")
    with st.form("form_turma"):
        nome_turma = st.text_input("Nome da turma")
        sala = st.text_input("Sala")
        disciplina_escolhida = st.selectbox("Disciplina", ["-- Selecione --"] + disciplinas)
        submit = st.form_submit_button("Guardar")

    if submit:
        if nome_turma.strip() == "" or sala.strip() == "" or disciplina_escolhida == "-- Selecione --":
            st.error("Por favor, preencha todos os campos antes de guardar.")
        else:
            sheet_turmas.append_row([nome_turma, sala, disciplina_escolhida])
            st.success(f"Turma '{nome_turma}' na sala '{sala}' associada à disciplina '{disciplina_escolhida}' adicionada ao Google Sheets!")

    st.divider()
    st.subheader("Lista de turmas")

    # Ler dados
    dados = sheet_turmas.get_all_records()

    if dados:
        df = pd.DataFrame(dados)

        # Pesquisa
        pesquisa = st.text_input("Pesquisar turma por nome, sala ou disciplina:")
        if pesquisa:
            df_filtrado = df[df.apply(lambda row: pesquisa.lower() in row.astype(str).str.lower().to_string(), axis=1)]
        else:
            df_filtrado = df

        # Listagem com botões
        for i, row in df_filtrado.iterrows():
            col1, col2, col3 = st.columns([4, 2, 2])
            col1.write(f"**{row['Nome da Turma']}** — Sala {row['Sala']} — {row['Disciplina']}")
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
                sheet_turmas.delete_rows(idx+2)
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
                nova_disciplina = st.selectbox("Disciplina", disciplinas, index=disciplinas.index(df.iloc[idx]['Disciplina']) if df.iloc[idx]['Disciplina'] in disciplinas else 0)
                guardar = st.form_submit_button("Guardar alterações")
            if guardar:
                sheet_turmas.update_cell(idx+2, 1, novo_nome)       # Coluna 1 = Nome da Turma
                sheet_turmas.update_cell(idx+2, 2, nova_sala)       # Coluna 2 = Sala
                sheet_turmas.update_cell(idx+2, 3, nova_disciplina) # Coluna 3 = Disciplina
                del st.session_state['edit_turma_index']
                st.rerun()

    else:
        st.info("Ainda não existem turmas registadas.")
