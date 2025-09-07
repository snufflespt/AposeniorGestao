import streamlit as st
import pandas as pd
import time
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
        with st.form("form_turma", clear_on_submit=True):
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
        dados = sheet_turmas.get_all_records()

        if not dados:
            st.info("Ainda não existem turmas registadas.")
        else:
            df = pd.DataFrame(dados)

            # --- VISTA DE EDIÇÃO ---
            if 'edit_turma_index' in st.session_state:
                idx = st.session_state['edit_turma_index']
                turma_atual = df.loc[idx]

                if st.button("⬅️ Voltar à lista"):
                    del st.session_state['edit_turma_index']
                    st.rerun()
                
                st.subheader(f"Editar turma: {turma_atual['Nome da Turma']}")
                with st.form("form_editar_turma"):
                    novo_nome = st.text_input("Nome da turma", value=turma_atual['Nome da Turma'])
                    nova_sala = st.text_input("Sala", value=turma_atual.get('Sala', ''))
                    
                    disciplina_atual = turma_atual.get('Disciplina')
                    disciplina_idx = disciplinas.index(disciplina_atual) if disciplina_atual in disciplinas else 0
                    nova_disciplina = st.selectbox("Disciplina", disciplinas, index=disciplina_idx)

                    if st.form_submit_button("Guardar alterações"):
                        sheet_turmas.update_cell(idx + 2, 1, novo_nome)
                        sheet_turmas.update_cell(idx + 2, 2, nova_sala)
                        sheet_turmas.update_cell(idx + 2, 3, nova_disciplina)
                        
                        st.success(f"Turma '{novo_nome}' atualizada com sucesso!")
                        del st.session_state['edit_turma_index']
                        time.sleep(0.5)
                        st.rerun()

            # --- VISTA DE APAGAR ---
            elif 'delete_turma_index' in st.session_state:
                idx = st.session_state['delete_turma_index']
                entity_name = df.loc[idx, 'Nome da Turma']

                if st.button("⬅️ Voltar à lista"):
                    del st.session_state['delete_turma_index']
                    st.rerun()

                st.subheader("Apagar turma")
                st.warning(f"Tens a certeza que queres apagar a turma: {entity_name}?")
                
                col1, col2, _ = st.columns([1, 1, 5])
                with col1:
                    if st.button("Sim, apagar", type="primary"):
                        sheet_turmas.delete_rows(idx + 2)
                        st.success(f"Turma '{entity_name}' apagada com sucesso!")
                        del st.session_state['delete_turma_index']
                        time.sleep(0.5)
                        st.rerun()
                with col2:
                    if st.button("Cancelar"):
                        del st.session_state['delete_turma_index']
                        st.rerun()

            # --- VISTA DE LISTA ---
            else:
                titulo_secao("Lista de turmas", "📋")
                pesquisa = st.text_input("Pesquisar por nome, sala ou disciplina:")

                if pesquisa:
                    df_filtrado = df[df.apply(lambda row: any(pesquisa.lower() in str(x).lower() for x in row), axis=1)]
                else:
                    df_filtrado = df

                for i, row in df_filtrado.iterrows():
                    with st.container(border=True):
                        st.text_input("Nome da Turma", value=row.get('Nome da Turma', ''), key=f"disp_nome_{i}", disabled=True)
                        st.text_input("Sala", value=row.get('Sala', ''), key=f"disp_sala_{i}", disabled=True)
                        st.text_input("Disciplina", value=row.get('Disciplina', ''), key=f"disp_disc_{i}", disabled=True)
                        
                        st.write("")

                        botoes_col1, botoes_col2, _ = st.columns([1, 1, 5])
                        with botoes_col1:
                            if st.button("✏️ Editar", key=f"edit_turma_{i}", use_container_width=True):
                                st.session_state['edit_turma_index'] = i
                                st.rerun()
                        with botoes_col2:
                            if st.button("🗑️ Apagar", key=f"delete_turma_{i}", use_container_width=True):
                                st.session_state['delete_turma_index'] = i
                                st.rerun()
                    
                    st.write("")
