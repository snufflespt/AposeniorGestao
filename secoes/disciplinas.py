import streamlit as st
import pandas as pd
import time
from datetime import date
from utils.sheets import get_worksheet
from utils.ui import titulo_secao
from utils.components import render_confirmation_dialog
from utils.validation import normalize_string

def mostrar_pagina():
    st.title("📚 Gestão de Disciplinas")
    if 'form_disc_key' not in st.session_state:
        st.session_state.form_disc_key = 0

    sheet = get_worksheet("Disciplinas")

    tab_adicionar, tab_gerir = st.tabs(["➕ Adicionar disciplina", "📋 Gerir disciplinas"])

    # -----------------------
    # Tab: Adicionar
    # -----------------------
    with tab_adicionar:
        titulo_secao("Adicionar nova disciplina", "➕")
        # Container com classe para destacar
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        with st.form(f"form_disciplina_{st.session_state.form_disc_key}"):
            nome_disc = st.text_input("**✍️ Nome da disciplina**", help="Campo obrigatório")
            estado = st.selectbox("🚦 Estado", ["Ativa", "Inativa"])
            observacoes = st.text_area("📋 Descrição/Observações")
            
            botoes_col1, botoes_col2, _ = st.columns([1, 1, 5])
            with botoes_col1:
                submit_guardar = st.form_submit_button("Guardar", type="primary")
            with botoes_col2:
                submit_limpar = st.form_submit_button("Limpar")

        if submit_limpar:
            st.session_state.form_disc_key += 1
            st.rerun()

        if submit_guardar:
            if not nome_disc.strip():
                st.error("O nome da disciplina é obrigatório.")
            else:
                dados_atuais = sheet.get_all_records()
                # Validar nome duplicado (ignorando maiúsculas/minúsculas e acentos)
                nomes_existentes = [normalize_string(d.get('Nome da Disciplina', '')) for d in dados_atuais]
                if normalize_string(nome_disc) in nomes_existentes:
                    st.error(f"A disciplina '{nome_disc}' já existe. Por favor, escolha um nome diferente.")
                else:
                    # Gerar ID sequencial (ex: D0001)
                    if not dados_atuais:
                        proximo_id_num = 1
                    else:
                        max_id = 0
                        for registo in dados_atuais:
                            try:
                                id_num = int(registo.get('id_disciplina', 'D0').split('D')[-1])
                                if id_num > max_id:
                                    max_id = id_num
                            except (ValueError, TypeError, IndexError):
                                continue
                        proximo_id_num = max_id + 1

                    novo_id = f"D{proximo_id_num:04d}"
                    data_criacao = date.today().strftime('%d/%m/%Y')

                    # Ordem: id_disciplina, Nome da Disciplina, Estado, Data de criacao, Descrição/Observacoes
                    sheet.append_row([novo_id, nome_disc, estado, data_criacao, observacoes])
                    st.success(f"Disciplina '{nome_disc}' adicionada com sucesso!")
                    st.session_state.form_disc_key += 1
                    st.rerun()

        # Fechar o container destaque
        st.markdown('</div>', unsafe_allow_html=True)

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
                    st.text_input("🆔 ID da Disciplina", value=disciplina_atual.get('id_disciplina', ''), disabled=True)
                    st.text_input("🗓️ Data de Criação", value=disciplina_atual.get('Data de criacao', ''), disabled=True)
                    
                    novo_nome = st.text_input("**✍️ Nome da disciplina**", value=disciplina_atual.get('Nome da Disciplina', ''), help="Campo obrigatório")
                    
                    estado_options = ["Ativa", "Inativa"]
                    estado_atual = disciplina_atual.get('Estado', 'Ativa')
                    estado_index = estado_options.index(estado_atual) if estado_atual in estado_options else 0
                    novo_estado = st.selectbox("🚦 Estado", estado_options, index=estado_index)
                    
                    nova_obs = st.text_area("📋 Descrição/Observações", value=disciplina_atual.get('Descrição/Observacoes', ''))

                    if st.form_submit_button("Guardar alterações"):
                        if not novo_nome.strip():
                            st.error("O nome da disciplina é obrigatório.")
                        else:
                            dados_atuais = sheet.get_all_records()
                            nome_duplicado = False
                            # Validar nome duplicado, ignorando o registo atual
                            for i, registo in enumerate(dados_atuais):
                                if i != idx and normalize_string(registo.get('Nome da Disciplina', '')) == normalize_string(novo_nome):
                                    nome_duplicado = True
                                    break
                            
                            if nome_duplicado:
                                st.error(f"A disciplina '{novo_nome}' já existe. Por favor, escolha um nome diferente.")
                            else:
                                # Ordem na folha: id_disciplina, Nome da Disciplina, Estado, Data de criacao, Descrição/Observacoes
                                # Atualizar da coluna B até E
                                valores = [
                                    novo_nome,
                                    novo_estado,
                                    disciplina_atual.get('Data de criacao', ''), # Manter data original
                                    nova_obs
                                ]
                                sheet.update(f'B{idx + 2}:E{idx + 2}', [valores])

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
                
                def confirm_delete():
                    sheet.delete_rows(idx + 2)
                    st.success(f"Disciplina '{entity_name}' apagada com sucesso!")
                    del st.session_state['delete_disc_index']
                    time.sleep(0.5)
                    st.rerun()

                def cancel_delete():
                    del st.session_state['delete_disc_index']
                    st.rerun()

                render_confirmation_dialog('disciplina', entity_name, confirm_delete, cancel_delete)

            # --- VISTA DE LISTA ---
            else:
                titulo_secao("Gerir disciplinas", "📋")
                pesquisa = st.text_input("Pesquisar por ID, nome, estado ou descrição:")
                
                if pesquisa:
                    df_filtrado = df[df.apply(
                        lambda row: any(pesquisa.lower() in str(x).lower() for x in row),
                        axis=1
                    )]
                else:
                    df_filtrado = df

                for i, row in df_filtrado.iterrows():
                    expander_title = f"📚 **{row.get('Nome da Disciplina', 'Sem Nome')}**"
                    # Container com destaque azul para disciplinar e expanders
                    st.markdown('<div class="card-container disciplina-container">', unsafe_allow_html=True)
                    with st.expander(expander_title):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.text_input("🆔 ID da Disciplina", value=row.get('id_disciplina', ''), key=f"disp_id_{i}", disabled=True)
                            st.text_input("🚦 Estado", value=row.get('Estado', ''), key=f"disp_estado_{i}", disabled=True)
                        with col2:
                            st.text_input("🗓️ Data de Criação", value=row.get('Data de criacao', ''), key=f"disp_data_{i}", disabled=True)

                        st.text_area("📋 Descrição/Observações", value=row.get('Descrição/Observacoes', ''), key=f"disp_obs_{i}", disabled=True)

                        st.write("---")

                        botoes_col1, botoes_col2, _ = st.columns([1, 1, 5])
                        with botoes_col1:
                            if st.button("✏️ Editar", key=f"edit_disc_{i}", use_container_width=True):
                                st.session_state['edit_disc_index'] = i
                                st.rerun()
                        with botoes_col2:
                            if st.button("🗑️ Apagar", key=f"delete_disc_{i}", use_container_width=True):
                                st.session_state['delete_disc_index'] = i
                                st.rerun()
                    # Fechar o container destaque
                    st.markdown('</div>', unsafe_allow_html=True)
