import streamlit as st
import pandas as pd
from utils.sheets import get_worksheet
from utils.ui import configurar_pagina, titulo_secao

def mostrar_pagina():
    configurar_pagina("Gestão de Professores", "👨‍🏫")

    sheet_prof = get_worksheet("Professores")
    sheet_disc = get_worksheet("Disciplinas")

    disciplinas = sheet_disc.col_values(1)[1:]

    tab_adicionar, tab_gerir = st.tabs(["➕ Adicionar professor", "📋 Gerir professores"])

    with tab_adicionar:
        titulo_secao("Adicionar novo professor", "➕")
        with st.form("form_professor"):
            col1, col2 = st.columns(2)
            with col1:
                nome_prof = st.text_input("Nome do professor")
                contacto = st.text_input("Contacto")
            with col2:
                disciplina = st.selectbox("Disciplina", ["-- Selecione --"] + disciplinas)
            submit = st.form_submit_button("Guardar")

        if submit:
            if nome_prof.strip() == "" or disciplina == "-- Selecione --":
                st.error("Por favor, preencha os campos obrigatórios.")
            else:
                sheet_prof.append_row([nome_prof, contacto, disciplina])
                st.success(f"Professor '{nome_prof}' adicionado com sucesso!")

    with tab_gerir:
        titulo_secao("Lista de professores", "📋")
        dados = sheet_prof.get_all_records()

        if dados:
            df = pd.DataFrame(dados)
            pesquisa = st.text_input("Pesquisar por nome, contacto ou disciplina:")

            if pesquisa:
                df_filtrado = df[df.apply(lambda row: pesquisa.lower() in row.astype(str).str.lower().to_string(), axis=1)]
            else:
                df_filtrado = df

            for i, row in df_filtrado.iterrows():
                col1, col2, col3 = st.columns([4, 2, 2])
                col1.write(f"**{row.get('Nome do Professor','')}** — {row.get('Disciplina','')}")
                if col2.button("✏️ Editar", key=f"edit_prof_{i}"):
                    st.session_state['edit_prof_index'] = i
                if col3.button("🗑️ Apagar", key=f"delete_prof_{i}"):
                    st.session_state['delete_prof_index'] = i

            if 'delete_prof_index' in st.session_state:
                idx = st.session_state['delete_prof_index']
                st.warning(f"Tens a certeza que queres apagar o professor: {df.iloc[idx]['Nome do Professor']}?")
                col_conf1, col_conf2 = st.columns(2)
                if col_conf1.button("✅ Sim, apagar"):
                    sheet_prof.delete_rows(idx+2)
                    del st.session_state['delete_prof_index']
                    st.rerun()
                if col_conf2.button("❌ Cancelar"):
                    del st.session_state['delete_prof_index']
                    st.rerun()

            if 'edit_prof_index' in st.session_state:
                idx = st.session_state['edit_prof_index']
                st.subheader("Editar professor")
                with st.form("form_editar_prof"):
                    novo_nome = st.text_input("Nome do professor", value=df.iloc[idx]['Nome do Professor'])
                    novo_contacto = st.text_input("Contacto", value=df.iloc[idx]['Contacto'])
                    nova_disciplina = st.selectbox("Disciplina", disciplinas, index=disciplinas.index(df.iloc[idx]['Disciplina']) if df.iloc[idx]['Disciplina'] in disciplinas else 0)
                    guardar = st.form_submit_button("Guardar alterações")
                if guardar:
                    sheet_prof.update_cell(idx+2, 1, novo_nome)
                    sheet_prof.update_cell(idx+2, 2, novo_contacto)
                    sheet_prof.update_cell(idx+2, 3, nova_disciplina)
                    del st.session_state['edit_prof_index']
                    st.rerun()
        else:
            st.info("Ainda não existem professores registados.")
