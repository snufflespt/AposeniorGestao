import streamlit as st
import pandas as pd
from utils.sheets import get_worksheet
from utils.ui import configurar_pagina, titulo_secao

def mostrar_pagina():
    configurar_pagina("Gestão de Disciplinas", "📚")

    sheet = get_worksheet("Disciplinas")

    # Tabs
    tab_adicionar, tab_gerir = st.tabs(["➕ Adicionar disciplina", "📋 Gerir disciplinas"])

    # -----------------------
    # Tab: Adicionar
    # -----------------------
    with tab_adicionar:
        titulo_secao("Adicionar nova disciplina", "➕")
        with st.form("form_disciplina"):
            col1, col2 = st.columns(2)
            with col1:
                nome_disc = st.text_input("Nome da disciplina")
                codigo = st.text_input("Código")
            with col2:
                descricao = st.text_area("Descrição")
            submit = st.form_submit_button("Guardar")

        if submit:
            if nome_disc.strip() == "":
                st.error("O nome da disciplina é obrigatório.")
            else:
                sheet.append_row([nome_disc, codigo, descricao])
                st.success(f"Disciplina '{nome_disc}' adicionada com sucesso!")

    # -----------------------
    # Tab: Gerir
    # -----------------------
    with tab_gerir:
        titulo_secao("Lista de disciplinas", "📋")
        dados = sheet.get_all_records()

        if dados:
            df = pd.DataFrame(dados)

            # Pesquisa
            pesquisa = st.text_input("Pesquisar por nome, código ou descrição:")
            if pesquisa:
                df_filtrado = df[df.apply(
                    lambda row: pesquisa.lower() in row.astype(str).str.lower().to_string(),
                    axis=1
                )]
            else:
                df_filtrado = df

            # Listagem com ações
            for i, row in df_filtrado.iterrows():
    col1, col2, col3 = st.columns([6, 1, 1])
    nome = row.get('Nome da Disciplina', '')
    cod = row.get('Código', '')
    col1.write(f"**{nome}** — {cod}")
    if col2.button("✏️ Editar", key=f"edit_disc_{i}", width="stretch"):
        st.session_state['edit_disc_index'] = i
    if col3.button("🗑️ Apagar", key=f"delete_disc_{i}", width="stretch"):
        st.session_state['delete_disc_index'] = i



            # Apagar com confirmação
            if 'delete_disc_index' in st.session_state:
                idx = st.session_state['delete_disc_index']
                st.warning(f"Tens a certeza que queres apagar a disciplina: {df.iloc[idx]['Nome da Disciplina']}?")
                col_conf1, col_conf2 = st.columns(2)
                if col_conf1.button("✅ Sim, apagar"):
                    sheet.delete_rows(idx+2)  # +2 por causa do cabeçalho
                    del st.session_state['delete_disc_index']
                    st.rerun()
                if col_conf2.button("❌ Cancelar"):
                    del st.session_state['delete_disc_index']
                    st.rerun()

            # Edição
            if 'edit_disc_index' in st.session_state:
                idx = st.session_state['edit_disc_index']
                st.subheader("Editar disciplina")
                with st.form("form_editar_disc"):
                    novo_nome = st.text_input("Nome da disciplina", value=df.iloc[idx]['Nome da Disciplina'])
                    novo_codigo = st.text_input("Código", value=df.iloc[idx]['Código'])
                    nova_desc = st.text_area("Descrição", value=df.iloc[idx]['Descrição'])
                    guardar = st.form_submit_button("Guardar alterações")
                if guardar:
                    sheet.update_cell(idx+2, 1, novo_nome)   # Coluna 1 = Nome da Disciplina
                    sheet.update_cell(idx+2, 2, novo_codigo) # Coluna 2 = Código
                    sheet.update_cell(idx+2, 3, nova_desc)   # Coluna 3 = Descrição
                    del st.session_state['edit_disc_index']
                    st.rerun()
        else:
            st.info("Ainda não existem disciplinas registadas.")
