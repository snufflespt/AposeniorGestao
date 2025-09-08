import streamlit as st
import pandas as pd
import time
import re
from datetime import date, datetime
from utils.sheets import get_worksheet
from utils.ui import configurar_pagina, titulo_secao
from utils.components import (
    render_confirmation_dialog, render_action_buttons
)

# --- Funções de Validação ---
def is_valid_phone(phone):
    """Verifica se o número de telefone tem 9 dígitos (ignorando espaços)."""
    if not phone: return True # Campo opcional, válido se vazio
    cleaned_phone = phone.replace(" ", "")
    return cleaned_phone.isdigit() and len(cleaned_phone) == 9

def is_valid_nif(nif):
    """Verifica se o NIF tem 9 dígitos."""
    if not nif: return True # A obrigatoriedade é verificada noutro lado
    return str(nif).strip().isdigit() and len(str(nif).strip()) == 9

def is_valid_postal_code(pc):
    """Verifica se o código postal está no formato XXXX-XXX."""
    if not pc: return True # A obrigatoriedade é verificada noutro lado
    return bool(re.match(r'^\d{4}-\d{3}$', pc.strip()))

def is_valid_email(email):
    """Verifica se o formato do email é válido."""
    if not email: return True # Campo opcional, válido se vazio
    return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email.strip()))

GRAU_ESCOLARIDADE_OPCOES = [
    "Sem Escolaridade", "1º Ciclo (4ª classe)", "2º Ciclo (6º ano)", 
    "3º Ciclo (9º ano)", "Ensino Secundário (12º ano)", "Licenciatura", 
    "Mestrado", "Doutoramento", "Outro"
]

SITUACAO_PROFISSIONAL_OPCOES = [
    "Ativo", "Desempregado", "Estudante", "Reformado", "Doméstico/a", "Outra"
]

def parse_date(date_str: str):
    """Converte uma string de data (DD/MM/YYYY) para um objeto date, ou retorna None."""
    if not date_str or not isinstance(date_str, str):
        return None
    try:
        return datetime.strptime(date_str, '%d/%m/%Y').date()
    except ValueError:
        return None

def mostrar_pagina():
    configurar_pagina("Gestão de Utentes", "🧍")

    if 'form_add_key' not in st.session_state:
        st.session_state.form_add_key = 0

    sheet = get_worksheet("Utentes")

    # Criar tabs
    tab_adicionar, tab_gerir = st.tabs(["➕ Adicionar utente", "📋 Gerir utentes"])

    with tab_adicionar:
        titulo_secao("Adicionar novo utente", "➕")
        with st.form(f"form_utente_{st.session_state.form_add_key}"):
            with st.expander("👤 Informação Pessoal", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    nome = st.text_input("**👤 Nome do utente**", help="Campo obrigatório")
                    data_nascimento = st.date_input("**🎂 Data de nascimento**", value=None, min_value=date(1920, 1, 1), format="DD/MM/YYYY", help="Campo obrigatório")
                    naturalidade = st.text_input("🌍 Naturalidade")
                with col2:
                    nacionalidade = st.text_input("🌍 Nacionalidade")
                    grau_escolaridade = st.selectbox("🎓 Grau de Escolaridade", options=GRAU_ESCOLARIDADE_OPCOES)
                    profissao = st.text_input("💼 Profissão")
                    situacao_profissional = st.selectbox("📈 Situação Profissional", options=SITUACAO_PROFISSIONAL_OPCOES)

            with st.expander("📞 Contactos e Morada"):
                col1, col2 = st.columns(2)
                with col1:
                    contacto_telefónico = st.text_input("**📞 Contacto telefónico**", help="Campo obrigatório")
                    contacto_telefónico_2 = st.text_input("📱 Contacto telefónico 2")
                    email = st.text_input("📧 Email")
                with col2:
                    morada = st.text_input("**🏠 Morada**", help="Campo obrigatório")
                    codigo_postal = st.text_input("**📮 Código Postal**", help="Campo obrigatório. Formato: XXXX-XXX")
                    localidade = st.text_input("📍 Localidade")

            with st.expander("💳 Documentos de Identificação"):
                col1, col2 = st.columns(2)
                with col1:
                    cartao_cidadao = st.text_input("💳 Cartão de Cidadão")
                    cc_validade = st.date_input("🗓️ Validade do CC", value=None, format="DD/MM/YYYY")
                    nif = st.text_input("**🧾 NIF**", help="Campo obrigatório")
                with col2:
                    niss = st.text_input("🧾 NISS")
                    cartao_utente = st.text_input("🏥 Cartão de Utente")

            with st.expander("👨‍👩‍👧‍👦 Informação Familiar e Administrativa"):
                col1, col2 = st.columns(2)
                with col1:
                    familiar = st.text_input("👨‍👩‍👧‍👦 Familiar")
                    telefone_familiar = st.text_input("📞 Telefone do Familiar")
                with col2:
                    data_inscricao = st.date_input("✍️ Data de inscrição", value=date.today(), format="DD/MM/YYYY")
                    estado = st.selectbox("🚦 Estado", ["Ativo", "Inativo"])
                observacoes = st.text_area("📋 Observações")

            botoes_col1, botoes_col2, _ = st.columns([1, 1, 5])
            with botoes_col1:
                submit_guardar = st.form_submit_button("Guardar Utente", type="primary")
            with botoes_col2:
                submit_limpar = st.form_submit_button("Limpar")

        if submit_limpar:
            st.session_state.form_add_key += 1
            st.rerun()

        if submit_guardar:
            # --- Validação de Campos ---
            campos_obrigatorios = {
                "Nome": nome, "Data de nascimento": data_nascimento,
                "Contacto telefónico": contacto_telefónico, "Morada": morada,
                "Código Postal": codigo_postal, "NIF": nif
            }
            campos_em_falta = [campo for campo, valor in campos_obrigatorios.items() if not valor]
            
            validation_errors = []
            if not is_valid_phone(contacto_telefónico): validation_errors.append("Contacto telefónico inválido (deve ter 9 dígitos).")
            if not is_valid_phone(contacto_telefónico_2): validation_errors.append("Contacto telefónico 2 inválido (deve ter 9 dígitos).")
            if not is_valid_phone(telefone_familiar): validation_errors.append("Telefone do Familiar inválido (deve ter 9 dígitos).")
            if not is_valid_nif(nif): validation_errors.append("NIF inválido (deve ter 9 dígitos).")
            if not is_valid_postal_code(codigo_postal): validation_errors.append("Código Postal inválido (formato esperado: XXXX-XXX).")
            if not is_valid_email(email): validation_errors.append("Email com formato inválido.")

            if campos_em_falta:
                st.error(f"Por favor, preencha os seguintes campos obrigatórios: {', '.join(campos_em_falta)}")
            elif validation_errors:
                st.error("Por favor, corrija os seguintes erros:\n- " + "\n- ".join(validation_errors))
            else:
                # Validar NIF duplicado
                dados_atuais = sheet.get_all_records()
                nifs_existentes = [str(registo.get('NIF', '')).strip() for registo in dados_atuais if str(registo.get('NIF', '')).strip()]
                
                if nif and str(nif).strip() in nifs_existentes:
                    st.error(f"O NIF '{nif}' já está associado a outro utente. Por favor, verifique os dados.")
                elif adicionar_utente(
                    sheet, nome, data_nascimento, naturalidade, nacionalidade,
                    contacto_telefónico, contacto_telefónico_2, email, morada,
                    codigo_postal, localidade, cartao_cidadao, cc_validade, nif,
                    niss, cartao_utente, telefone_familiar, familiar,
                    grau_escolaridade, profissao, situacao_profissional,
                    data_inscricao, observacoes, estado
                ):
                    st.success(f"Utente '{nome}' adicionado com sucesso!")
                    st.session_state.form_add_key += 1
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

                    with st.expander("👤 Informação Pessoal", expanded=True):
                        col1, col2 = st.columns(2)
                        with col1:
                            novo_nome = st.text_input("**👤 Nome do utente**", value=utente_atual.get('Nome', ''), help="Campo obrigatório")
                            nova_data_nascimento = st.date_input("**🎂 Data de nascimento**", value=parse_date(utente_atual.get('Data_de_nascimento')), min_value=date(1920, 1, 1), format="DD/MM/YYYY", help="Campo obrigatório")
                            nova_naturalidade = st.text_input("🌍 Naturalidade", value=utente_atual.get('Naturalidade', ''))
                        with col2:
                            nova_nacionalidade = st.text_input("🌍 Nacionalidade", value=utente_atual.get('Nacionalidade', ''))
                            
                            grau_atual = utente_atual.get('Grau_Escolaridade', '')
                            grau_idx = GRAU_ESCOLARIDADE_OPCOES.index(grau_atual) if grau_atual in GRAU_ESCOLARIDADE_OPCOES else 0
                            novo_grau_escolaridade = st.selectbox("🎓 Grau de Escolaridade", options=GRAU_ESCOLARIDADE_OPCOES, index=grau_idx)
                            
                            nova_profissao = st.text_input("💼 Profissão", value=utente_atual.get('Profissao', ''))

                            situacao_atual = utente_atual.get('Situacao_Profissional', '')
                            situacao_idx = SITUACAO_PROFISSIONAL_OPCOES.index(situacao_atual) if situacao_atual in SITUACAO_PROFISSIONAL_OPCOES else 0
                            nova_situacao_profissional = st.selectbox("📈 Situação Profissional", options=SITUACAO_PROFISSIONAL_OPCOES, index=situacao_idx)

                    with st.expander("📞 Contactos e Morada"):
                        col1, col2 = st.columns(2)
                        with col1:
                            novo_contacto_telefónico = st.text_input("**📞 Contacto telefónico**", value=utente_atual.get('Contacto_telefónico', ''), help="Campo obrigatório")
                            novo_contacto_telefónico_2 = st.text_input("📱 Contacto telefónico 2", value=utente_atual.get('Contacto_telefónico_2', ''))
                            novo_email = st.text_input("📧 Email", value=utente_atual.get('Email', ''))
                        with col2:
                            nova_morada = st.text_input("**🏠 Morada**", value=utente_atual.get('Morada', ''), help="Campo obrigatório")
                            novo_codigo_postal = st.text_input("**📮 Código Postal**", value=utente_atual.get('Codigo_Postal', ''), help="Campo obrigatório. Formato: XXXX-XXX")
                            nova_localidade = st.text_input("📍 Localidade", value=utente_atual.get('Localidade', ''))

                    with st.expander("💳 Documentos de Identificação"):
                        col1, col2 = st.columns(2)
                        with col1:
                            novo_cartao_cidadao = st.text_input("💳 Cartão de Cidadão", value=utente_atual.get('Cartao_Cidadao', ''))
                            nova_cc_validade = st.date_input("🗓️ Validade do CC", value=parse_date(utente_atual.get('CC_Validade')), format="DD/MM/YYYY")
                            novo_nif = st.text_input("**🧾 NIF**", value=utente_atual.get('NIF', ''), help="Campo obrigatório")
                        with col2:
                            novo_niss = st.text_input("🧾 NISS", value=utente_atual.get('NISS', ''))
                            novo_cartao_utente = st.text_input("🏥 Cartão de Utente", value=utente_atual.get('Cartao_Utente', ''))

                    with st.expander("👨‍👩‍👧‍👦 Informação Familiar e Administrativa"):
                        col1, col2 = st.columns(2)
                        with col1:
                            novo_familiar = st.text_input("👨‍👩‍👧‍👦 Familiar", value=utente_atual.get('Familiar', ''))
                            novo_telefone_familiar = st.text_input("📞 Telefone do Familiar", value=utente_atual.get('Telefone_Familiar', ''))
                        with col2:
                            nova_data_inscricao = st.date_input("✍️ Data de inscrição", value=parse_date(utente_atual.get('Data de inscrição')), format="DD/MM/YYYY")
                            
                            estado_options = ["Ativo", "Inativo"]
                            estado_atual = utente_atual.get('Estado', 'Ativo')
                            estado_index = estado_options.index(estado_atual) if estado_atual in estado_options else 0
                            novo_estado = st.selectbox("🚦 Estado", estado_options, index=estado_index)
                        
                        novo_observacoes = st.text_area("📋 Observações", value=utente_atual.get('Observacoes', ''))
                    
                    if st.form_submit_button("Guardar alterações"):
                        # --- Validação de Campos ---
                        campos_obrigatorios = {
                            "Nome": novo_nome, "Data de nascimento": nova_data_nascimento,
                            "Contacto telefónico": novo_contacto_telefónico, "Morada": nova_morada,
                            "Código Postal": novo_codigo_postal, "NIF": novo_nif
                        }
                        campos_em_falta = [campo for campo, valor in campos_obrigatorios.items() if not valor]

                        validation_errors = []
                        if not is_valid_phone(novo_contacto_telefónico): validation_errors.append("Contacto telefónico inválido (deve ter 9 dígitos).")
                        if not is_valid_phone(novo_contacto_telefónico_2): validation_errors.append("Contacto telefónico 2 inválido (deve ter 9 dígitos).")
                        if not is_valid_phone(novo_telefone_familiar): validation_errors.append("Telefone do Familiar inválido (deve ter 9 dígitos).")
                        if not is_valid_nif(novo_nif): validation_errors.append("NIF inválido (deve ter 9 dígitos).")
                        if not is_valid_postal_code(novo_codigo_postal): validation_errors.append("Código Postal inválido (formato esperado: XXXX-XXX).")
                        if not is_valid_email(novo_email): validation_errors.append("Email com formato inválido.")

                        if campos_em_falta:
                            st.error(f"Por favor, preencha os seguintes campos obrigatórios: {', '.join(campos_em_falta)}")
                        elif validation_errors:
                            st.error("Por favor, corrija os seguintes erros:\n- " + "\n- ".join(validation_errors))
                        else:
                            # Validar NIF duplicado
                            dados_atuais = sheet.get_all_records()
                            nif_duplicado = False
                            if novo_nif:
                                for i_registo, registo in enumerate(dados_atuais):
                                    # Verifica se o NIF existe e pertence a um utente diferente do que está a ser editado
                                    if str(registo.get('NIF', '')).strip() == str(novo_nif).strip() and i_registo != idx:
                                        st.error(f"O NIF '{novo_nif}' já está associado a outro utente. Por favor, verifique os dados.")
                                        nif_duplicado = True
                                        break
                            
                            if not nif_duplicado:
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
                                    'Data de inscrição': nova_data_inscricao, 'Observacoes': novo_observacoes, 
                                    'Estado': novo_estado
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
                    # Título do expander apenas com o nome do utente
                    expander_title = f"👤 **{row.get('Nome', 'Sem Nome')}**"
                    with st.expander(expander_title):
                        # Detalhes do utente organizados em secções
                        with st.expander("👤 Informação Pessoal"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.text_input("👤 Nome", value=row.get('Nome', ''), key=f"disp_nome_{i}", disabled=True)
                                st.text_input("🎂 Data de nascimento", value=row.get('Data_de_nascimento', ''), key=f"disp_data_nasc_{i}", disabled=True)
                                st.text_input("🌍 Naturalidade", value=row.get('Naturalidade', ''), key=f"disp_naturalidade_{i}", disabled=True)
                            with col2:
                                st.text_input("🌍 Nacionalidade", value=row.get('Nacionalidade', ''), key=f"disp_nacionalidade_{i}", disabled=True)
                                st.text_input("🎓 Grau de Escolaridade", value=row.get('Grau_Escolaridade', ''), key=f"disp_grau_{i}", disabled=True)
                                st.text_input("💼 Profissão", value=row.get('Profissao', ''), key=f"disp_profissao_{i}", disabled=True)
                            st.text_input("📈 Situação Profissional", value=row.get('Situacao_Profissional', ''), key=f"disp_situacao_{i}", disabled=True)

                        with st.expander("📞 Contactos e Morada"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.text_input("📞 Contacto telefónico", value=row.get('Contacto_telefónico', ''), key=f"disp_contacto1_{i}", disabled=True)
                                st.text_input("📱 Contacto telefónico 2", value=row.get('Contacto_telefónico_2', ''), key=f"disp_contacto2_{i}", disabled=True)
                                st.text_input("📧 Email", value=row.get('Email', ''), key=f"disp_email_{i}", disabled=True)
                            with col2:
                                st.text_input("🏠 Morada", value=row.get('Morada', ''), key=f"disp_morada_{i}", disabled=True)
                                st.text_input("📮 Código Postal", value=row.get('Codigo_Postal', ''), key=f"disp_cp_{i}", disabled=True)
                                st.text_input("📍 Localidade", value=row.get('Localidade', ''), key=f"disp_localidade_{i}", disabled=True)

                        with st.expander("💳 Documentos de Identificação"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.text_input("💳 Cartão de Cidadão", value=row.get('Cartao_Cidadao', ''), key=f"disp_cc_{i}", disabled=True)
                                st.text_input("🗓️ Validade do CC", value=row.get('CC_Validade', ''), key=f"disp_cc_val_{i}", disabled=True)
                                st.text_input("🧾 NIF", value=row.get('NIF', ''), key=f"disp_nif_{i}", disabled=True)
                            with col2:
                                st.text_input("🧾 NISS", value=row.get('NISS', ''), key=f"disp_niss_{i}", disabled=True)
                                st.text_input("🏥 Cartão de Utente", value=row.get('Cartao_Utente', ''), key=f"disp_utente_doc_{i}", disabled=True)

                        with st.expander("👨‍👩‍👧‍👦 Informação Familiar e Administrativa"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.text_input("👨‍👩‍👧‍👦 Familiar", value=row.get('Familiar', ''), key=f"disp_familiar_{i}", disabled=True)
                                st.text_input("📞 Telefone do Familiar", value=row.get('Telefone_Familiar', ''), key=f"disp_tel_familiar_{i}", disabled=True)
                            with col2:
                                st.text_input("✍️ Data de inscrição", value=row.get('Data de inscrição', ''), key=f"disp_data_insc_{i}", disabled=True)
                                st.text_input("🚦 Estado", value=row.get('Estado', ''), key=f"disp_estado_{i}", disabled=True)
                        
                        st.text_area("📋 Observações", value=row.get('Observacoes', ''), key=f"disp_obs_{i}", disabled=True)
                        
                        st.write("---")

                        # Botões de ação
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


# Funções auxiliares para operações CRUD
def adicionar_utente(sheet, nome, data_nascimento, naturalidade, nacionalidade,
                   contacto_telefónico, contacto_telefónico_2, email, morada,
                   codigo_postal, localidade, cartao_cidadao, cc_validade, nif,
                   niss, cartao_utente, telefone_familiar, familiar,
                   grau_escolaridade, profissao, situacao_profissional,
                   data_inscricao, observacoes, estado) -> bool:
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

        # Formatar datas para string (DD/MM/YYYY) ou string vazia
        def format_date(d):
            return d.strftime('%d/%m/%Y') if d else ""

        nova_linha = [
            novo_id, nome, format_date(data_nascimento), naturalidade, nacionalidade,
            contacto_telefónico, contacto_telefónico_2, email, morada,
            codigo_postal, localidade, cartao_cidadao, format_date(cc_validade), nif,
            niss, cartao_utente, telefone_familiar, familiar,
            grau_escolaridade, profissao, situacao_profissional,
            format_date(data_inscricao), observacoes, estado
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
            return d.strftime('%d/%m/%Y') if d else ""

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
            format_date(dados.get('Data de inscrição')), dados.get('Observacoes', ''), 
            dados.get('Estado', 'Ativo')
        ]
        
        # Atualizar da coluna B (Nome) até à coluna X (Estado)
        sheet.update(f'B{index + 2}:X{index + 2}', [values])
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
