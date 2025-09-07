import streamlit as st
import pandas as pd
import time
from utils.sheets import get_worksheet
from utils.ui import configurar_pagina, titulo_secao

def mostrar_pagina():
    configurar_pagina("Gestão de Disciplinas", "📚")

    sheet = get_worksheet("Disciplinas")

    tab_adicionar, tab_gerir = st.tabs(["➕ Adicionar disciplina", "📋 Gerir disciplinas"])

    # -----------------------
    # Tab: Adicionar
    # -----------------------
    with tab_adicionar:
        titulo_secao("Adicionar nova disciplina", "➕")
        with st.form("form_disciplina", clear_on_submit=True):
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
        dados = sheet.get_all_records()

        if not dados:
            st.info("Ainda não existem disciplinas registadas.")
        else:
            df = pd.DataFrame(dados)

            # --- VISTA DE EDIÇÃO ---
            if 'edit_disc_index' in st.session_state:
                idx = st.session_state['edit_disc_index']
                disciplina_atual = df.loc[idx]

                if st.button("⬅️ Voltar à lista"):
                    del st.session_state['edit_disc_index']
                    st.rerun()

                st.subheader(f"Editar disciplina: {disciplina_atual['Nome da Disciplina']}")
                with st.form("form_editar_disc"):
                    novo_nome = st.text_input("Nome da disciplina", value=disciplina_atual['Nome da Disciplina'])
                    novo_codigo = st.text_input("Código", value=disciplina_atual.get('Código', ''))
                    nova_desc = st.text_area("Descrição", value=disciplina_atual.get('Descrição', ''))
                    
                    if st.form_submit_button("Guardar alterações"):
                        sheet.update_cell(idx + 2, 1, novo_nome)
                        sheet.update_cell(idx + 2, 2, novo_codigo)
                        sheet.update_cell(idx + 2, 3, nova_desc)
                        
                        st.success(f"Disciplina '{novo_nome}' atualizada com sucesso!")
                        del st.session_state['edit_disc_index']
                        time.sleep(0.5)
                        st.rerun()

            # --- VISTA DE APAGAR ---
            elif 'delete_disc_index' in st.session_state:
                idx = st.session_state['delete_disc_index']
                entity_name = df.loc[idx, 'Nome da Disciplina']

                if st.button("⬅️ Voltar à lista"):
                    del st.session_state['delete_disc_index']
                    st.rerun()

                st.subheader("Apagar disciplina")
                st.warning(f"Tens a certeza que queres apagar a disciplina: {entity_name}?")
                
                col1, col2, _ = st.columns([1, 1, 5])
                with col1:
                    if st.button("Sim, apagar", type="primary"):
                        sheet.delete_rows(idx + 2)
                        st.success(f"Disciplina '{entity_name}' apagada com sucesso!")
                        del st.session_state['delete_disc_index']
                        time.sleep(0.5)
                        st.rerun()
                with col2:
                    if st.button("Cancelar"):
                        del st.session_state['delete_disc_index']
                        st.rerun()

            # --- VISTA DE LISTA ---
            else:
                titulo_secao("Gerir disciplinas", "📋")
                pesquisa = st.text_input("Pesquisar por nome, código ou descrição:")
                
                if pesquisa:
                    df_filtrado = df[df.apply(
                        lambda row: any(pesquisa.lower() in str(x).lower() for x in row),
                        axis=1
                    )]
                else:
                    df_filtrado = df

                for i, row in df_filtrado.iterrows():
                    with st.container(border=True):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.text_input("Nome da disciplina", value=row.get('Nome da Disciplina', ''), key=f"disp_nome_{i}", disabled=True)
                            st.text_input("Código", value=row.get('Código', ''), key=f"disp_codigo_{i}", disabled=True)
                        with col2:
                            st.text_area("Descrição", value=row.get('Descrição', ''), key=f"disp_desc_{i}", disabled=True, height=129)

                        st.write("") 

                        botoes_col1, botoes_col2, _ = st.columns([1, 1, 5])
                        with botoes_col1:
                            if st.button("✏️ Editar", key=f"edit_disc_{i}", use_container_width=True):
                                st.session_state['edit_disc_index'] = i
                                st.rerun()
                        with botoes_col2:
                            if st.button("🗑️ Apagar", key=f"delete_disc_{i}", use_container_width=True):
                                st.session_state['delete_disc_index'] = i
                                st.rerun()
                    
                    st.write("")
