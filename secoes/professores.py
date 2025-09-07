import streamlit as st
import pandas as pd
import time
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
        with st.form("form_professor", clear_on_submit=True):
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
        dados = sheet_prof.get_all_records()

        if not dados:
            st.info("Ainda não existem professores registados.")
        else:
            df = pd.DataFrame(dados)

            # --- VISTA DE EDIÇÃO ---
            if 'edit_prof_index' in st.session_state:
                idx = st.session_state['edit_prof_index']
                prof_atual = df.loc[idx]

                if st.button("⬅️ Voltar à lista"):
                    del st.session_state['edit_prof_index']
                    st.rerun()
                
                st.subheader(f"Editar professor: {prof_atual['Nome do Professor']}")
                with st.form("form_editar_prof"):
                    novo_nome = st.text_input("Nome do professor", value=prof_atual['Nome do Professor'])
                    novo_contacto = st.text_input("Contacto", value=prof_atual.get('Contacto', ''))
                    
                    disciplina_atual = prof_atual.get('Disciplina')
                    disciplina_idx = disciplinas.index(disciplina_atual) if disciplina_atual in disciplinas else 0
                    nova_disciplina = st.selectbox("Disciplina", disciplinas, index=disciplina_idx)

                    if st.form_submit_button("Guardar alterações"):
                        sheet_prof.update_cell(idx + 2, 1, novo_nome)
                        sheet_prof.update_cell(idx + 2, 2, novo_contacto)
                        sheet_prof.update_cell(idx + 2, 3, nova_disciplina)
                        
                        st.success(f"Professor '{novo_nome}' atualizado com sucesso!")
                        del st.session_state['edit_prof_index']
                        time.sleep(0.5)
                        st.rerun()

            # --- VISTA DE APAGAR ---
            elif 'delete_prof_index' in st.session_state:
                idx = st.session_state['delete_prof_index']
                entity_name = df.loc[idx, 'Nome do Professor']

                if st.button("⬅️ Voltar à lista"):
                    del st.session_state['delete_prof_index']
                    st.rerun()

                st.subheader("Apagar professor")
                st.warning(f"Tens a certeza que queres apagar o professor: {entity_name}?")
                
                col1, col2, _ = st.columns([1, 1, 5])
                with col1:
                    if st.button("Sim, apagar", type="primary"):
                        sheet_prof.delete_rows(idx + 2)
                        st.success(f"Professor '{entity_name}' apagado com sucesso!")
                        del st.session_state['delete_prof_index']
                        time.sleep(0.5)
                        st.rerun()
                with col2:
                    if st.button("Cancelar"):
                        del st.session_state['delete_prof_index']
                        st.rerun()

            # --- VISTA DE LISTA ---
            else:
                titulo_secao("Lista de professores", "📋")
                pesquisa = st.text_input("Pesquisar por nome, contacto ou disciplina:")

                if pesquisa:
                    df_filtrado = df[df.apply(lambda row: any(pesquisa.lower() in str(x).lower() for x in row), axis=1)]
                else:
                    df_filtrado = df

                for i, row in df_filtrado.iterrows():
                    with st.container(border=True):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.text_input("Nome do Professor", value=row.get('Nome do Professor', ''), key=f"disp_nome_{i}", disabled=True)
                        with col2:
                            st.text_input("Contacto", value=row.get('Contacto', ''), key=f"disp_contacto_{i}", disabled=True)
                        
                        st.text_input("Disciplina", value=row.get('Disciplina', ''), key=f"disp_disc_{i}", disabled=True)
                        
                        st.write("")

                        botoes_col1, botoes_col2, _ = st.columns([1, 1, 5])
                        with botoes_col1:
                            if st.button("✏️ Editar", key=f"edit_prof_{i}", use_container_width=True):
                                st.session_state['edit_prof_index'] = i
                                st.rerun()
                        with botoes_col2:
                            if st.button("🗑️ Apagar", key=f"delete_prof_{i}", use_container_width=True):
                                st.session_state['delete_prof_index'] = i
                                st.rerun()
                    
                    st.write("")
