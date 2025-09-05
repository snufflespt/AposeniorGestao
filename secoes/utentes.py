import streamlit as st
import pandas as pd
from utils.sheets import get_worksheet
from utils.ui import configurar_pagina, titulo_secao

def mostrar_pagina():
    configurar_pagina("Gestão de Utentes", "🧍")

    sheet = get_worksheet("Utentes")

    # Criar tabs
    tab_adicionar, tab_gerir = st.tabs(["➕ Adicionar utente", "📋 Gerir utentes"])

    with tab_adicionar:
        titulo_secao("Adicionar novo utente", "➕")
        with st.form("form_utente"):
            col1, col2 = st.columns(2)
            with col1:
                nome = st.text_input("Nome do utente")
                contacto = st.text_input("Contacto")
            with col2:
                morada = st.text_input("Morada")
                estado = st.selectbox("Estado", ["Ativo", "Inativo"])
            submit = st.form_submit_button("Guardar")

        if submit:
            if nome.strip() == "" or contacto.strip() == "":
                st.error("Por favor, preencha os campos obrigatórios.")
            else:
                sheet.append_row([nome, contacto, morada, estado])
                st.success(f"Utente '{nome}' adicionado com sucesso!")

    with tab_gerir:
        titulo_secao("Lista de utentes", "📋")
        dados = sheet.get_all_records()

        if dados:
            df = pd.DataFrame(dados)
            pesquisa = st.text_input("Pesquisar utente por qualquer campo:")

            if pesquisa:
                df_filtrado = df[df.apply(lambda row: pesquisa.lower() in row.astype(str).str.lower().to_string(), axis=1)]
            else:
                df_filtrado = df

            for i, row in df_filtrado.iterrows():
                col1, col2, col3 = st.columns([6, 1, 1])
                col1.write(f"**{row['Nome']}** — {row['Contacto']}")
                if col2.button("✏️ Editar", key=f"edit_{i}"):
                    st.session_state['edit_index'] = i
                if col3.button("🗑️ Apagar", key=f"delete_{i}"):
                    st.session_state['delete_index'] = i

            if 'delete_index' in st.session_state:
                idx = st.session_state['delete_index']
                st.warning(f"Tens a certeza que queres apagar o utente: {df.iloc[idx]['Nome']}?")
                col_conf1, col_conf2 = st.columns(2)
                if col_conf1.button("✅ Sim, apagar"):
                    sheet.delete_rows(idx+2)
                    del st.session_state['delete_index']
                    st.rerun()
                if col_conf2.button("❌ Cancelar"):
                    del st.session_state['delete_index']
                    st.rerun()

            if 'edit_index' in st.session_state:
                idx = st.session_state['edit_index']
                st.subheader("Editar utente")
                with st.form("form_editar"):
                    novo_nome = st.text_input("Nome do utente", value=df.iloc[idx]['Nome'])
                    novo_contacto = st.text_input("Contacto", value=df.iloc[idx]['Contacto'])
                    nova_morada = st.text_input("Morada", value=df.iloc[idx].get('Morada', ''))
                    novo_estado = st.selectbox("Estado", ["Ativo", "Inativo"], index=["Ativo", "Inativo"].index(df.iloc[idx].get('Estado', 'Ativo')))
                    guardar = st.form_submit_button("Guardar alterações")
                if guardar:
                    sheet.update_cell(idx+2, 1, novo_nome)
                    sheet.update_cell(idx+2, 2, novo_contacto)
                    sheet.update_cell(idx+2, 3, nova_morada)
                    sheet.update_cell(idx+2, 4, novo_estado)
                    del st.session_state['edit_index']
                    st.rerun()
        else:
            st.info("Ainda não existem utentes registados.")
