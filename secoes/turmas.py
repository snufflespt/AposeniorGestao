import streamlit as st
import pandas as pd
from utils.sheets import get_worksheet
from utils.ui import configurar_pagina, titulo_secao

def mostrar_pagina():
    configurar_pagina("Gestão de Turmas", "🏫")

    sheet_turmas = get_worksheet("Turmas")
    sheet_disc = get_worksheet("Disciplinas")

    # Obter lista de disciplinas
    disciplinas = sheet_disc.col_values(1)[1:]  # Ignora cabeçalho

    tab_adicionar, tab_gerir = st.tabs(["➕ Adicionar turma", "📋 Gerir turmas"])

    with tab_adicionar:
        titulo_secao("Adicionar nova turma", "➕")
        with st.form("form_turma"):
            col1, col2 = st.columns(2)
            with col1:
                nome_turma = st.text_input("Nome da turma")
                sala = st.text_input("Sala")
            with col2:
                disciplina_escolhida = st.selectbox("Disciplina", ["-- Selecione --"] + disciplinas)
            submit = st.form_submit_button("Guardar")

        if submit:
            if nome_turma.strip() == "" or sala.strip() == "" or disciplina_escolhida == "-- Selecione --":
                st.error("Por favor, preencha todos os campos antes de guardar.")
            else:
                sheet_turmas.append_row([nome_turma, sala, disciplina_escolhida])
                st.success(f"Turma '{nome_turma}' adicionada com sucesso!")

    with tab_gerir:
        titulo_secao("Lista de turmas", "📋")
        dados = sheet_turmas.get_all_records()

        if dados:
            df = pd.DataFrame(dados)
            pesquisa = st.text_input("Pesquisar por nome, sala ou disciplina:")

            if pesquisa:
                df_filtrado = df[df.apply(lambda row: pesquisa.lower() in row.astype(str).str.lower().to_string(), axis=1)]
            else:
                df_filtrado = df

            for i, row in df_filtrado.iterrows():
                col1, col2, col3 = st.columns([6, 1, 1])
                col1.write(f"**{row.get('Nome da Turma','')}** — Sala {row.get('Sala','')} — {row.get('Disciplina','')}")
                if col2.button("✏️ Editar", key=f"edit_turma_{i}"):
                    st.session_state['edit_turma_index'] = i
                if col3.button("🗑️ Apagar", key=f"delete_turma_{i}"):
                    st.session_state['delete_turma_index'] = i

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

            if 'edit_turma_index' in st.session_state:
                idx = st.session_state['edit_turma_index']
                st.subheader("Editar turma")
                with st.form("form_editar_turma"):
                    novo_nome = st.text_input("Nome da turma", value=df.iloc[idx]['Nome da Turma'])
                    nova_sala = st.text_input("Sala", value=df.iloc[idx]['Sala'])
                    nova_disciplina = st.selectbox("Disciplina", disciplinas, index=disciplinas.index(df.iloc[idx]['Disciplina']) if df.iloc[idx]['Disciplina'] in disciplinas else 0)
                    guardar = st.form_submit_button("Guardar alterações")
                if guardar:
                    sheet_turmas.update_cell(idx+2, 1, novo_nome)
                    sheet_turmas.update_cell(idx+2, 2, nova_sala)
                    sheet_turmas.update_cell(idx+2, 3, nova_disciplina)
                    del st.session_state['edit_turma_index']
                    st.rerun()
        else:
            st.info("Ainda não existem turmas registadas.")
