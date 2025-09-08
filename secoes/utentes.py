import streamlit as st
import pandas as pd
import time
from datetime import date, datetime
from utils.sheets import get_worksheet
from utils.ui import configurar_pagina, titulo_secao
from utils.components import (
    render_confirmation_dialog, render_action_buttons
)

def parse_date(date_str: str):
    """Converte uma string de data (YYYY-MM-DD) para um objeto date, ou retorna None."""
    if not date_str or not isinstance(date_str, str):
        return None
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return None

def mostrar_pagina():
    configurar_pagina("Gestão de Utentes", "🧍")

    sheet = get_worksheet("Utentes")

    # Criar tabs
    tab_adicionar, tab_gerir = st.tabs(["➕ Adicionar utente", "📋 Gerir utentes"])

    with tab_adicionar:
        titulo_secao("Adicionar novo utente", "➕")
        with st.form("form_utente", clear_on_submit=True):
            with st.expander("Informação Pessoal", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    nome = st.text_input("**Nome do utente**", help="Campo obrigatório")
                    data_nascimento = st.date_input("Data de nascimento", value=None)
                    naturalidade = st.text_input("Naturalidade")
                with col2:
                    nacionalidade = st.text_input("Nacionalidade")
                    grau_escolaridade = st.text_input("Grau de Escolaridade")
                    profissao = st.text_input("Profissão")
                    situacao_profissional = st.text_input("Situação Profissional")

            with st.expander("Contactos e Morada"):
                col1, col2 = st.columns(2)
                with col1:
                    contacto_telefónico = st.text_input("**Contacto telefónico**", help="Campo obrigatório")
                    contacto_telefónico_2 = st.text_input("Contacto telefónico 2")
                    email = st.text_input("Email")
                with col2:
                    morada = st.text_input("Morada")
                    codigo_postal = st.text_input("Código Postal")
                    localidade = st.text_input("Localidade")

            with st.expander("Documentos de Identificação"):
                col1, col2 = st.columns(2)
                with col1:
                    cartao_cidadao = st.text_input("Cartão de Cidadão")
                    cc_validade = st.date_input("Validade do CC", value=None)
                    nif = st.text_input("NIF")
                with col2:
                    niss = st.text_input("NISS")
                    cartao_utente = st.text_input("Cartão de Utente")

            with st.expander("Informação Familiar e Administrativa"):
                col1, col2 = st.columns(2)
                with col1:
                    familiar = st.text_input("Familiar")
                    telefone_familiar = st.text_input("Telefone do Familiar")
                with col2:
                    data_inscricao = st.date_input("Data de inscrição", value=date.today())
                    estado = st.selectbox("Estado", ["Ativo", "Inativo"])

            submit = st.form_submit_button("Guardar Utente")

        if submit:
            if not nome or not contacto_telefónico:
                st.error("Por favor, preencha os campos obrigatórios (Nome e Contacto telefónico).")
            else:
                if adicionar_utente(
                    sheet, nome, data_nascimento, naturalidade, nacionalidade,
                    contacto_telefónico, contacto_telefónico_2, email, morada,
                    codigo_postal, localidade, cartao_cidadao, cc_validade, nif,
                    niss, cartao_utente, telefone_familiar, familiar,
                    grau_escolaridade, profissao, situacao_profissional,
                    data_inscricao, estado
                ):
                    st.success(f"Utente '{nome}' adicionado com sucesso!")
                    st.rerun()

    with tab_gerir:
        dados = sheet.get_all_records()

        if not dados:
            st.info("Ainda não existem utentes registados.")
        else:
            df = pd.DataFrame(dados)

            # --- VISTA DE EDIÇÃO ---
            if 'edit_index' in st.session_state:
                idx = st.session_state['edit_index']
                utente_atual = df.loc[idx]

                if st.button("⬅️ Voltar à lista"):
                    del st.session_state['edit_index']
                    st.rerun()

                st.subheader(f"Editar utente: {utente_atual['Nome']}")

                with st.form("form_editar"):
                    st.text_input("ID", value=utente_atual.get('ID', ''), disabled=True)

                    with st.expander("Informação Pessoal", expanded=True):
                        col1, col2 = st.columns(2)
                        with col1:
                            novo_nome = st.text_input("**Nome do utente**", value=utente_atual.get('Nome', ''))
                            nova_data_nascimento = st.date_input("Data de nascimento", value=parse_date(utente_atual.get('Data_de_nascimento')))
                            nova_naturalidade = st.text_input("Naturalidade", value=utente_atual.get('Naturalidade', ''))
                        with col2:
                            nova_nacionalidade = st.text_input("Nacionalidade", value=utente_atual.get('Nacionalidade', ''))
                            novo_grau_escolaridade = st.text_input("Grau de Escolaridade", value=utente_atual.get('Grau_Escolaridade', ''))
                            nova_profissao = st.text_input("Profissão", value=utente_atual.get('Profissao', ''))
                            nova_situacao_profissional = st.text_input("Situação Profissional", value=utente_atual.get('Situacao_Profissional', ''))

                    with st.expander("Contactos e Morada"):
                        col1, col2 = st.columns(2)
                        with col1:
                            novo_contacto_telefónico = st.text_input("**Contacto telefónico**", value=utente_atual.get('Contacto_telefónico', ''))
                            novo_contacto_telefónico_2 = st.text_input("Contacto telefónico 2", value=utente_atual.get('Contacto_telefónico_2', ''))
                            novo_email = st.text_input("Email", value=utente_atual.get('Email', ''))
                        with col2:
                            nova_morada = st.text_input("Morada", value=utente_atual.get('Morada', ''))
                            novo_codigo_postal = st.text_input("Código Postal", value=utente_atual.get('Codigo_Postal', ''))
                            nova_localidade = st.text_input("Localidade", value=utente_atual.get('Localidade', ''))

                    with st.expander("Documentos de Identificação"):
                        col1, col2 = st.columns(2)
                        with col1:
                            novo_cartao_cidadao = st.text_input("Cartão de Cidadão", value=utente_atual.get('Cartao_Cidadao', ''))
                            nova_cc_validade = st.date_input("Validade do CC", value=parse_date(utente_atual.get('CC_Validade')))
                            novo_nif = st.text_input("NIF", value=utente_atual.get('NIF', ''))
                        with col2:
                            novo_niss = st.text_input("NISS", value=utente_atual.get('NISS', ''))
                            novo_cartao_utente = st.text_input("Cartão de Utente", value=utente_atual.get('Cartao_Utente', ''))

                    with st.expander("Informação Familiar e Administrativa"):
                        col1, col2 = st.columns(2)
                        with col1:
                            novo_familiar = st.text_input("Familiar", value=utente_atual.get('Familiar', ''))
                            novo_telefone_familiar = st.text_input("Telefone do Familiar", value=utente_atual.get('Telefone_Familiar', ''))
                        with col2:
                            nova_data_inscricao = st.date_input("Data de inscrição", value=parse_date(utente_atual.get('Data de inscrição')))
                            
                            estado_options = ["Ativo", "Inativo"]
                            estado_atual = utente_atual.get('Estado', 'Ativo')
                            estado_index = estado_options.index(estado_atual) if estado_atual in estado_options else 0
                            novo_estado = st.selectbox("Estado", estado_options, index=estado_index)
                    
                    if st.form_submit_button("Guardar alterações"):
                        novos_dados = {
                            'Nome': novo_nome, 'Data_de_nascimento': nova_data_nascimento,
                            'Naturalidade': nova_naturalidade, 'Nacionalidade': nova_nacionalidade,
                            'Contacto_telefónico': novo_contacto_telefónico,
                            'Contacto_telefónico_2': novo_contacto_telefónico_2, 'Email': novo_email,
                            'Morada': nova_morada, 'Codigo_Postal': novo_codigo_postal,
                            'Localidade': nova_localidade, 'Cartao_Cidadao': novo_cartao_cidadao,
                            'CC_Validade': nova_cc_validade, 'NIF': novo_nif, 'NISS': novo_niss,
                            'Cartao_Utente': novo_cartao_utente,
                            'Telefone_Familiar': novo_telefone_familiar, 'Familiar': novo_familiar,
                            'Grau_Escolaridade': novo_grau_escolaridade, 'Profissao': nova_profissao,
                            'Situacao_Profissional': nova_situacao_profissional,
                            'Data de inscrição': nova_data_inscricao, 'Estado': novo_estado
                        }

                        if atualizar_utente(sheet, idx, novos_dados):
                            st.success(f"Utente '{novo_nome}' atualizado com sucesso!")
                            del st.session_state['edit_index']
                            time.sleep(0.5)
                            st.rerun()
            
            # --- VISTA DE APAGAR ---
            elif 'delete_index' in st.session_state:
                idx = st.session_state['delete_index']
                entity_name = df.loc[idx, 'Nome']

                if st.button("⬅️ Voltar à lista"):
                    del st.session_state['delete_index']
                    st.rerun()

                st.subheader("Apagar utente")
                
                def confirm_delete():
                    if apagar_utente(sheet, idx):
                        st.success(f"Utente '{entity_name}' apagado com sucesso!")
                        del st.session_state['delete_index']
                        time.sleep(0.5)
                        st.rerun()

                def cancel_delete():
                    del st.session_state['delete_index']
                    st.rerun()

                render_confirmation_dialog('utente', entity_name, confirm_delete, cancel_delete)

            # --- VISTA DE LISTA ---
            else:
                st.markdown("### Lista de utentes")
                pesquisa = st.text_input("Pesquisar utente por qualquer campo:")

                if pesquisa:
                    df_filtrado = df[df.apply(lambda row: any(pesquisa.lower() in str(x).lower() for x in row), axis=1)]
                else:
                    df_filtrado = df

                for i, row in df_filtrado.iterrows():
                    with st.container(border=True):
                        st.text_input("ID", value=row.get('ID', ''), key=f"disp_id_{i}", disabled=True)
                        col1, col2 = st.columns(2)
                        with col1:
                            st.text_input("Nome do utente", value=row.get('Nome', ''), key=f"disp_nome_{i}", disabled=True)
                            st.text_input("Contacto", value=row.get('Contacto', ''), key=f"disp_contacto_{i}", disabled=True)
                        with col2:
                            st.text_input("Morada", value=row.get('Morada', ''), key=f"disp_morada_{i}", disabled=True)
                            st.text_input("Estado", value=row.get('Estado', ''), key=f"disp_estado_{i}", disabled=True)
                        
                        st.write("")

                        botoes_col1, botoes_col2, botoes_col3, _ = st.columns([1, 1, 1, 4])
                        with botoes_col1:
                            if st.button("✏️ Editar", key=f"edit_utente_{i}", use_container_width=True):
                                st.session_state['edit_index'] = i
                                st.rerun()
                        with botoes_col2:
                            if st.button("🗑️ Apagar", key=f"delete_utente_{i}", use_container_width=True):
                                st.session_state['delete_index'] = i
                                st.rerun()
                        with botoes_col3:
                            st.button("⚙️ Gerir", key=f"manage_utente_{i}", use_container_width=True)
                    
                    st.write("")


# Funções auxiliares para operações CRUD
def adicionar_utente(sheet, nome, data_nascimento, naturalidade, nacionalidade,
                   contacto_telefónico, contacto_telefónico_2, email, morada,
                   codigo_postal, localidade, cartao_cidadao, cc_validade, nif,
                   niss, cartao_utente, telefone_familiar, familiar,
                   grau_escolaridade, profissao, situacao_profissional,
                   data_inscricao, estado) -> bool:
    """Adiciona um novo utente à planilha com todos os campos."""
    try:
        # Gerar ID sequencial
        dados_atuais = sheet.get_all_records()
        if not dados_atuais:
            proximo_id_num = 1
        else:
            max_id = 0
            for registo in dados_atuais:
                try:
                    id_num = int(registo.get('ID', 0))
                    if id_num > max_id:
                        max_id = id_num
                except (ValueError, TypeError):
                    continue
            proximo_id_num = max_id + 1
        novo_id = f"{proximo_id_num:04d}"

        # Formatar datas para string (YYYY-MM-DD) ou string vazia
        def format_date(d):
            return d.strftime('%Y-%m-%d') if d else ""

        nova_linha = [
            novo_id, nome, format_date(data_nascimento), naturalidade, nacionalidade,
            contacto_telefónico, contacto_telefónico_2, email, morada,
            codigo_postal, localidade, cartao_cidadao, format_date(cc_validade), nif,
            niss, cartao_utente, telefone_familiar, familiar,
            grau_escolaridade, profissao, situacao_profissional,
            format_date(data_inscricao), estado
        ]
        
        sheet.append_row(nova_linha)
        return True
    except Exception as e:
        st.error(f"Erro ao adicionar utente: {str(e)}")
        return False

def atualizar_utente(sheet, index: int, dados: dict) -> bool:
    """Atualiza os dados de um utente na planilha."""
    try:
        def format_date(d):
            return d.strftime('%Y-%m-%d') if d else ""

        # A ordem deve corresponder exatamente à ordem das colunas na folha, a partir da coluna B
        values = [
            dados.get('Nome', ''), format_date(dados.get('Data_de_nascimento')),
            dados.get('Naturalidade', ''), dados.get('Nacionalidade', ''),
            dados.get('Contacto_telefónico', ''), dados.get('Contacto_telefónico_2', ''),
            dados.get('Email', ''), dados.get('Morada', ''),
            dados.get('Codigo_Postal', ''), dados.get('Localidade', ''),
            dados.get('Cartao_Cidadao', ''), format_date(dados.get('CC_Validade')),
            dados.get('NIF', ''), dados.get('NISS', ''),
            dados.get('Cartao_Utente', ''), dados.get('Telefone_Familiar', ''),
            dados.get('Familiar', ''), dados.get('Grau_Escolaridade', ''),
            dados.get('Profissao', ''), dados.get('Situacao_Profissional', ''),
            format_date(dados.get('Data de inscrição')), dados.get('Estado', 'Ativo')
        ]
        
        # Atualizar da coluna B (Nome) até à coluna W (Estado)
        sheet.update(f'B{index + 2}:W{index + 2}', [values])
        return True
    except Exception as e:
        st.error(f"Erro ao atualizar utente: {str(e)}")
        return False

def apagar_utente(sheet, index: int) -> bool:
    """
    Apaga um utente da planilha

    Args:
        sheet: Planilha do Google Sheets
        index: Índice do utente na planilha

    Returns:
        True se apagado com sucesso, False caso contrário
    """
    try:
        sheet.delete_rows(index + 2)
        return True
    except Exception as e:
        st.error(f"Erro ao apagar utente: {str(e)}")
        return False
