import streamlit as st
import pandas as pd
import time
import re
from utils.sheets import get_worksheet
from utils.ui import configurar_pagina, titulo_secao

def normalize_string(s: str) -> str:
    """Normaliza uma string para comparação, removendo espaços e convertendo para minúsculas."""
    return str(s).strip().lower()

def is_valid_phone(phone: str) -> bool:
    """Verifica se um número de telefone é válido (9 dígitos)."""
    if not phone:
        return True  # Permite campos vazios, a obrigatoriedade é validada à parte
    return re.match(r'^\d{9}$', phone)

def is_valid_email(email: str) -> bool:
    """Verifica se um email tem um formato válido."""
    if not email:
        return True  # Permite campos vazios
    return re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email)

def mostrar_pagina():
    configurar_pagina("Gestão de Professores", "👨‍🏫")

    sheet_prof = get_worksheet("Professores")

    tab_adicionar, tab_gerir = st.tabs(["➕ Adicionar professor", "📋 Gerir professores"])

    with tab_adicionar:
        titulo_secao("Adicionar novo professor", "➕")

        def clear_form_data():
            """Limpa os dados do formulário na session_state."""
            st.session_state.prof_nome = ""
            st.session_state.prof_telefone = ""
            st.session_state.prof_email = ""
            st.session_state.prof_nib = ""
            st.session_state.prof_valor_hora = 0.0
            st.session_state.prof_observacoes = ""

        with st.form("form_professor"):
            nome_completo = st.text_input("👤 **Nome Completo***", key="prof_nome")
            col1, col2 = st.columns(2)
            with col1:
                telefone = st.text_input("📞 **Telefone***", key="prof_telefone")
                nib = st.text_input("💳 NIB", key="prof_nib")
            with col2:
                email = st.text_input("📧 Email", key="prof_email")
                valor_hora = st.number_input(
                    "💶 Valor Hora (€)",
                    min_value=0.0,
                    step=0.5,
                    format="%.2f",
                    key="prof_valor_hora"
                )
            
            observacoes = st.text_area("📝 Observações", key="prof_observacoes")

            b_col1, b_col2, _ = st.columns([1, 1, 5])
            with b_col1:
                submit = st.form_submit_button("Guardar")
            with b_col2:
                if st.form_submit_button("Limpar"):
                    clear_form_data()
                    st.rerun()

        if submit:
            dados_professores = sheet_prof.get_all_records()
            df_prof = pd.DataFrame(dados_professores)
            
            erros = []
            if not nome_completo.strip():
                erros.append("O campo 'Nome Completo' é obrigatório.")
            if not telefone.strip():
                erros.append("O campo 'Telefone' é obrigatório.")
            if not is_valid_phone(telefone.strip()):
                erros.append("O formato do telefone é inválido (deve ter 9 dígitos).")
            if not is_valid_email(email.strip()):
                erros.append("O formato do email é inválido.")
            
            if not df_prof.empty and 'Nome Completo' in df_prof.columns and normalize_string(nome_completo) in df_prof['Nome Completo'].apply(normalize_string).values:
                erros.append(f"Já existe um professor com o nome '{nome_completo}'.")

            if erros:
                for erro in erros:
                    st.error(erro)
            else:
                if df_prof.empty or 'ID_professor' not in df_prof.columns or df_prof['ID_professor'].dropna().empty:
                    novo_id = "P0001"
                else:
                    ultimo_id = df_prof['ID_professor'].dropna().max()
                    ultimo_num = int(re.sub(r'\D', '', str(ultimo_id)))
                    novo_id_num = ultimo_num + 1
                    novo_id = f"P{novo_id_num:04d}"
                
                nova_linha = [novo_id, nome_completo, telefone, email, nib, float(valor_hora), observacoes]
                sheet_prof.append_row(nova_linha)
                st.success(f"Professor '{nome_completo}' adicionado com sucesso!")
                clear_form_data()
                time.sleep(1)
                st.rerun()

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
                
                st.subheader(f"Editar professor: {prof_atual['Nome Completo']}")
                with st.form("form_editar_prof"):
                    novo_nome = st.text_input("👤 **Nome Completo***", value=prof_atual.get('Nome Completo', ''))
                    col1, col2 = st.columns(2)
                    with col1:
                        novo_telefone = st.text_input("📞 **Telefone***", value=str(prof_atual.get('Telefone', '')))
                        novo_nib = st.text_input("💳 NIB", value=str(prof_atual.get('NIB', '')))
                    with col2:
                        novo_email = st.text_input("📧 Email", value=prof_atual.get('Email', ''))
                        novo_valor_hora = st.number_input("💶 Valor Hora (€)", min_value=0.0, step=0.5, format="%.2f", value=float(prof_atual.get('Valor Hora', 0.0)))
                    
                    novas_observacoes = st.text_area("📝 Observações", value=prof_atual.get('Observacoes', ''))

                    if st.form_submit_button("Guardar alterações"):
                        erros = []
                        if not novo_nome.strip():
                            erros.append("O campo 'Nome Completo' é obrigatório.")
                        if not novo_telefone.strip():
                            erros.append("O campo 'Telefone' é obrigatório.")
                        if not is_valid_phone(novo_telefone.strip()):
                            erros.append("O formato do telefone é inválido (deve ter 9 dígitos).")
                        if not is_valid_email(novo_email.strip()):
                            erros.append("O formato do email é inválido.")

                        df_outros = df.drop(index=idx)
                        if not df_outros.empty and 'Nome Completo' in df_outros.columns and normalize_string(novo_nome) in df_outros['Nome Completo'].apply(normalize_string).values:
                            erros.append(f"Já existe um professor com o nome '{novo_nome}'.")

                        if erros:
                            for erro in erros:
                                st.error(erro)
                        else:
                            # ID (col A) não é atualizado.
                            valores_a_atualizar = [
                                novo_nome, novo_telefone, novo_email, novo_nib, 
                                float(novo_valor_hora), novas_observacoes
                            ]
                            sheet_prof.update(f'B{idx + 2}:G{idx + 2}', [valores_a_atualizar])
                            
                            st.success(f"Professor '{novo_nome}' atualizado com sucesso!")
                            del st.session_state['edit_prof_index']
                            time.sleep(0.5)
                            st.rerun()

            # --- VISTA DE APAGAR ---
            elif 'delete_prof_index' in st.session_state:
                idx = st.session_state['delete_prof_index']
                entity_name = df.loc[idx, 'Nome Completo']

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
                pesquisa = st.text_input("Pesquisar por nome, telefone, email, etc.:")

                if pesquisa:
                    df_filtrado = df[df.apply(lambda row: any(pesquisa.lower() in str(x).lower() for x in row), axis=1)]
                else:
                    df_filtrado = df

                for i, row in df_filtrado.iterrows():
                    with st.container(border=True):
                        c1, c2 = st.columns([1, 4])
                        c1.text_input("🆔 ID", value=row.get('ID_professor', ''), key=f"disp_id_{i}", disabled=True)
                        c2.text_input("👤 Nome Completo", value=row.get('Nome Completo', ''), key=f"disp_nome_{i}", disabled=True)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.text_input("📞 Telefone", value=str(row.get('Telefone', '')), key=f"disp_tel_{i}", disabled=True)
                            st.text_input("💳 NIB", value=str(row.get('NIB', '')), key=f"disp_nib_{i}", disabled=True)
                        with col2:
                            st.text_input("📧 Email", value=row.get('Email', ''), key=f"disp_email_{i}", disabled=True)
                            st.text_input("💶 Valor Hora (€)", value=str(row.get('Valor Hora', '0.0')), key=f"disp_valor_{i}", disabled=True)
                        
                        st.text_area("📝 Observações", value=row.get('Observacoes', ''), key=f"disp_obs_{i}", disabled=True, height=100)

                        st.write("") # Espaçador

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
