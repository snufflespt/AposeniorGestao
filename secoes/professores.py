"""
Gestão de Professores - Aplicação AposeniorGestao

Este módulo fornece funcionalidade completa para gestão de professores,
incluindo criação, edição, visualização e remoção de registos de professores.
Utiliza as utilities centralizadas para manter consistência e reduzir duplicação de código.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any

# Importações das utilities centralizadas
from utils.ui import titulo_secao
from utils.crud import (
    get_sheet_data,
    SheetConfig,
    create_record,
    update_record,
    delete_record as delete_record_crud,
    search_and_filter_dataframe
)
from utils.validation import (
    validate_form_data,
    is_valid_phone,
    is_valid_email,
    normalize_string
)
from utils.components import (
    render_confirmation_dialog,
    render_data_display_card,
    render_search_and_filter,
    render_error_message
)

# ===== CONFIGURAÇÃO DA ENTIDADE =====

PROFESSOR_CONFIG = SheetConfig(
    name="Professores",
    id_column="ID_professor",
    id_prefix="P",
    required_columns=['Nome Completo', 'Telefone'],
    unique_columns=['Nome Completo'],
    conflict_rules={}
)

PROFESSOR_VALIDATION_RULES = {
    'Nome Completo': {'required': True, 'label': 'Nome Completo'},
    'Telefone': {'type': 'phone', 'required': True, 'label': 'Telefone'},
    'Email': {'type': 'email', 'label': 'Email'}
}

PROFESSOR_FIELD_NAMES = {
    'Nome Completo': 'Nome Completo',
    'Telefone': 'Telefone',
    'Email': 'Email',
    'NIB': 'NIB',
    'Valor Hora': '💰 Valor Hora (€)',
    'Observacoes': 'Observações'
}


def mostrar_pagina() -> None:
    """
    Renderiza a página principal de gestão de professores.

    Inclui formulários para adicionar/editar e listagem com funcionalidades
    de pesquisa e ações CRUD padronizadas.
    """
    st.title("👨‍🏫 Gestão de Professores")

    # Obter dados com cache
    professor_df = get_sheet_data("Professores")

    tab_adicionar, tab_gerir = st.tabs(["➕ Adicionar professor", "📋 Gerir professores"])

    with tab_adicionar:
        render_add_form(professor_df)

    with tab_gerir:
        render_management_section(professor_df)


def render_add_form(professor_df: pd.DataFrame) -> None:
    """
    Renderiza formulário para adicionar novo professor.

    Args:
        professor_df (pd.DataFrame): Dados existentes dos professores para validações.
    """
    titulo_secao("Adicionar novo professor", "➕")

    # Initialize form key if it doesn't exist
    if 'form_prof_key' not in st.session_state:
        st.session_state.form_prof_key = 0

    # Container com classe para destacar
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    with st.form(f"form_professor_{st.session_state.form_prof_key}"):
        form_data = {}

        # Configuração de campos com validações
        campos = [
            {'name': 'Nome Completo', 'label': '👤 Nome Completo', 'type': 'text_input', 'required': True},
            {'name': 'Telefone', 'label': '📞 Telefone', 'type': 'text_input', 'required': True},
            {'name': 'Email', 'label': '📧 Email', 'type': 'text_input'},
            {'name': 'NIB', 'label': '💳 NIB', 'type': 'text_input'},
            {'name': 'Valor Hora', 'label': '💰 Valor hora (€)', 'type': 'number_input',
             'min_value': 0.0, 'step': 0.5, 'format': '%.2f'},
            {'name': 'Observacoes', 'label': '📝 Observações', 'type': 'text_area'}
        ]

        for campo in campos:
            if campo['type'] == 'number_input':
                form_data[campo['name']] = st.number_input(
                    campo['label'],
                    value=0.0,
                    **{k: v for k, v in campo.items() if k not in ['name', 'label', 'type']}
                )
            elif campo['type'] == 'text_area':
                form_data[campo['name']] = st.text_area(campo['label'])
            else:
                form_data[campo['name']] = st.text_input(campo['label'])

        col_guardar, col_limpar = st.columns(2)
        with col_guardar:
            submetido = st.form_submit_button("✅ Guardar Professor", type="primary")
        with col_limpar:
            limpar = st.form_submit_button("🗑️ Limpar Formulário")

        # using the same working approach from disciplinas.py
        if limpar:
            st.session_state.form_prof_key += 1
            st.rerun()

        if submetido:
            if salvar_professor(form_data, professor_df):
                # Limpar formulário após sucesso
                for key in st.session_state:
                    if key.startswith('form_professor') or key in form_data:
                        if key in st.session_state:
                            del st.session_state[key]
                st.rerun()

    # Fechar o container destaque
    st.markdown('</div>', unsafe_allow_html=True)


def salvar_professor(form_data: Dict[str, Any], professor_df: pd.DataFrame) -> bool:
    """
    Processa e salva novo professor após validações.

    Args:
        form_data (Dict[str, Any]): Dados do formulário.
        professor_df (pd.DataFrame): Dados existentes para validações.

    Returns:
        bool: True se salvo com sucesso, False caso contrário.
    """
    # Validar formulário
    validation_errors = validate_form_data(form_data, PROFESSOR_VALIDATION_RULES)

    # Validar unicidade do nome
    if form_data.get('Nome Completo'):
        nome_normalizado = normalize_string(form_data['Nome Completo'])
        nomes_existentes = professor_df['Nome Completo'].apply(normalize_string).values

        if nome_normalizado in nomes_existentes:
            validation_errors.append("Já existe um professor com este nome.")

    if validation_errors:
        render_error_message("Por favor, corrija os erros abaixo:", validation_errors)
        return False

    # Tentar criar registo
    success = create_record(PROFESSOR_CONFIG, form_data,
                           success_message=f"Professor '{form_data['Nome Completo']}' adicionado com sucesso!")

    return success


def render_management_section(professor_df: pd.DataFrame) -> None:
    """
    Renderiza seção de gestão dos professores existentes.

    Args:
        professor_df (pd.DataFrame): Dados dos professores para exibição.
    """
    # Verificar vistas específicas (edição/apagamento)
    if verificar_vista_edicao(professor_df):
        return

    if verificar_vista_apagamento(professor_df):
        return

    # Vista de lista padrão
    render_lista_professores(professor_df)


def verificar_vista_edicao(professor_df: pd.DataFrame) -> bool:
    """
    Verifica e renderiza vista de edição se ativada.

    Args:
        professor_df (pd.DataFrame): Dados dos professores.

    Returns:
        bool: True se vista de edição foi renderizada.
    """
    if 'edit_prof_index' not in st.session_state:
        return False

    idx = st.session_state['edit_prof_index']
    if idx >= len(professor_df):
        del st.session_state['edit_prof_index']
        return False

    if st.button("⬅️ Voltar à lista", key="voltar_lista_prof"):
        del st.session_state['edit_prof_index']
        st.rerun()
        return True

    # Add form key initialization for edition form too
    if 'form_editar_prof_key' not in st.session_state:
        st.session_state.form_editar_prof_key = 0

    professor_atual = professor_df.iloc[idx]
    render_edit_form_professor(professor_atual, idx)
    return True


def render_edit_form_professor(professor_data: pd.Series, index: int) -> None:
    """
    Renderiza formulário de edição para professor específico.

    Args:
        professor_data (pd.Series): Dados do professor a editar.
        index (int): Índice do professor no DataFrame.
    """
    st.subheader(f"Editar professor: {professor_data['Nome Completo']}")

    with st.form(f"form_editar_prof_{st.session_state.form_editar_prof_key}"):
        form_data = {}

        col1, col2 = st.columns(2)
        with col1:
            form_data['Nome Completo'] = st.text_input(
                "👤 Nome Completo *",
                value=professor_data.get('Nome Completo', '')
            )
            form_data['Telefone'] = st.text_input(
                "📞 Telefone *",
                value=str(professor_data.get('Telefone', ''))
            )
            form_data['Email'] = st.text_input(
                "📧 Email",
                value=professor_data.get('Email', '')
            )
        with col2:
            form_data['NIB'] = st.text_input(
                "💳 NIB",
                value=str(professor_data.get('NIB', ''))
            )
            form_data['Valor Hora'] = st.number_input(
                "💰 Valor hora (€)",
                value=float(professor_data.get('Valor Hora', 0.0)),
                min_value=0.0,
                step=0.5,
                format="%.2f"
            )
            form_data['Observacoes'] = st.text_area(
                "📝 Observações",
                value=professor_data.get('Observacoes', '')
            )

        col_guardar_alteracoes, col_limpar_alteracoes = st.columns(2)
        with col_guardar_alteracoes:
            if st.form_submit_button("✅ Guardar Alterações", type="primary"):
                if atualizar_professor(form_data, index):
                    del st.session_state['edit_prof_index']
                    st.rerun()

        with col_limpar_alteracoes:
            if st.form_submit_button("🗑️ Limpar Alterações"):
                st.session_state.form_editar_prof_key += 1
                st.rerun()


def atualizar_professor(form_data: Dict[str, Any], index: int) -> bool:
    """
    Atualiza dados do professor após validações.

    Args:
        form_data (Dict[str, Any]): Novos dados do professor.
        index (int): Índice do professor no DataFrame.

    Returns:
        bool: True se atualizado com sucesso, False caso contrário.
    """
    # Validar formulário
    validation_errors = validate_form_data(form_data, PROFESSOR_VALIDATION_RULES)

    if validation_errors:
        render_error_message("Por favor, corrija os erros abaixo:", validation_errors)
        return False

    # Tentar atualizar registo (excluindo este registo das validações únicas)
    success = update_record(PROFESSOR_CONFIG, index, form_data,
                           success_message=f"Professor '{form_data['Nome Completo']}' atualizado com sucesso!")

    return success


def verificar_vista_apagamento(professor_df: pd.DataFrame) -> bool:
    """
    Verifica e renderiza vista de apagamento se ativada.

    Args:
        professor_df (pd.DataFrame): Dados dos professores.

    Returns:
        bool: True se vista de apagamento foi renderizada.
    """
    if 'delete_prof_index' not in st.session_state:
        return False

    idx = st.session_state['delete_prof_index']
    if idx >= len(professor_df):
        del st.session_state['delete_prof_index']
        return False

    professor_atual = professor_df.iloc[idx]

    if st.button("⬅️ Voltar à lista", key="voltar_lista_prof_delete"):
        del st.session_state['delete_prof_index']
        st.rerun()
        return True

    st.subheader("Apagar professor")

    def confirm_delete():
        sucesso = delete_record_crud(PROFESSOR_CONFIG, idx,
                                   success_message=f"Professor '{professor_atual['Nome Completo']}' apagado com sucesso!")
        if sucesso:
            del st.session_state['delete_prof_index']
        return sucesso

    def cancel_delete():
        del st.session_state['delete_prof_index']
        st.rerun()

    confirm_message = f"Tens a certeza que queres apagar o professor **{professor_atual['Nome Completo']}**?\n\nEsta ação não pode ser desfeita."
    render_confirmation_dialog('professor', str(professor_atual['Nome Completo']),
                              confirm_delete, cancel_delete)

    return True


def render_lista_professores(professor_df: pd.DataFrame) -> None:
    """
    Renderiza lista de professores com pesquisa e filtros.

    Args:
        professor_df (pd.DataFrame): Dados dos professores para exibir.
    """
    if professor_df.empty:
        st.info("👍 Ainda não existem professores registados.")
        st.markdown("**Dica:** Clique na aba '*Adicionar professor*' para criar o primeiro registo.")
        return

    titulo_secao("Lista de professores", "📋")

    # Pesquisa e filtro
    search_text = render_search_and_filter("Pesquisar por nome, telefone, email ou NIB...")

    # Aplicar filtros
    if search_text:
        masked_professor_df = professor_df.applymap(str)  # Para permitir string search
        mask = masked_professor_df.apply(lambda row: any(search_text.lower() in cell.lower() for cell in row),
                                        axis=1)
        filtered_df = professor_df[mask]
    else:
        filtered_df = professor_df

    if filtered_df.empty:
        st.info("Nenhum professor encontrado com os critérios de pesquisa.")
        return

    # Mostrar resultados
    st.write(f"**Mostrando {len(filtered_df)} de {len(professor_df)} professor(es)**")

    # Renderizar cartões de professores
    for i, professor_row in filtered_df.iterrows():
        render_professor_card(professor_row, i)


def render_professor_card(professor_data: pd.Series, index: int) -> None:
    """
    Renderiza cartão individual de professor com ações.

    Args:
        professor_data (pd.Series): Dados do professor.
        index (int): Índice original no DataFrame para ações.
    """
    nome_completo = professor_data.get('Nome Completo', 'Sem nome')
    id_professor = professor_data.get('ID_professor', f'idx_{index}')

    # Container com fundo azul-claro para destacar
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    with st.container():
        # Usar expander para melhor organização
        with st.expander(f"👨‍🏫 **{nome_completo}** ({id_professor})", expanded=False):

            # Layout com colunas para informação
            col_info, col_actions = st.columns([4, 1])

            with col_info:
                # Informações principais
                st.write(f"**🆔 ID:** {id_professor}")
                st.write(f"**📞 Telefone:** {professor_data.get('Telefone', 'N/A')}")
                if professor_data.get('Email'):
                    st.write(f"**📧 Email:** {professor_data.get('Email')}")

                col1, col2 = st.columns(2)
                with col1:
                    if professor_data.get('NIB'):
                        st.write(f"**💳 NIB:** {professor_data.get('NIB')}")
                with col2:
                    if professor_data.get('Valor Hora'):
                        valor_hora = float(professor_data.get('Valor Hora', 0))
                        if valor_hora > 0:
                            st.write(f"**💰 Valor/Hora:** {valor_hora:.2f}€")

                if professor_data.get('Observacoes'):
                    st.write("**📝 Observações:**")
                    st.write(professor_data.get('Observacoes'))

            with col_actions:
                # Botões de ação vertical
                if st.button("✏️ Editar", key=f"edit_prof_{index}", use_container_width=True):
                    st.session_state['edit_prof_index'] = index
                    st.rerun()

                if st.button("🗑️ Apagar", key=f"delete_prof_{index}", use_container_width=True):
                    st.session_state['delete_prof_index'] = index
                    st.rerun()

            st.divider()

    # Fechar o container destaque do card
    st.markdown('</div>', unsafe_allow_html=True)
