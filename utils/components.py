"""
Biblioteca de Componentes Reutilizáveis para Streamlit

Este módulo providencia componentes padronizados e reutilizáveis
para a aplicação Streamlit, incluindo formulários, cards, botões de ação,
e outros elementos de UI comuns para melhorar a manutenção e consistência.
"""

import streamlit as st
from typing import Dict, Any, Optional, Callable, List
from utils.validation import (
    GRAU_ESCOLARIDADE_OPCOES,
    SITUACAO_PROFISSIONAL_OPCOES,
    DIAS_SEMANA,
    SALA_OPCOES,
    NIVEL_OPCOES,
    ESTADO_OPCOES,
    format_status_badge,
    format_currency,
    format_date_for_display,
    format_time_for_display
)


def render_user_card(user_data: Dict[str, Any],
                     index: int,
                     on_edit: Optional[Callable] = None,
                     on_delete: Optional[Callable] = None) -> None:
    """Renderiza um card de utente com informações e botões de ação."""
    nome = user_data.get('Nome', '')
    contacto = user_data.get('Contacto', '')
    morada = user_data.get('Morada', '')
    estado = user_data.get('Estado', '')

    with st.container():
        col_info, col_actions = st.columns([4, 1])

        with col_info:
            st.markdown(f"**{nome}** — {contacto}")
            if morada:
                st.markdown(f"🏠 {morada}")
            st.markdown(format_status_badge(estado, 'Ativo'), unsafe_allow_html=True)

        with col_actions:
            render_action_buttons(index, on_edit, on_delete, 'utente')

        st.divider()


def render_action_buttons(index: int,
                         on_edit: Optional[Callable] = None,
                         on_delete: Optional[Callable] = None,
                         entity_type: str = "item") -> None:
    """Renderiza botões de ação padronizados (Editar/Apagar)."""
    sub_col1, sub_col2 = st.columns(2)

    with sub_col1:
        if st.button("✏️ Editar", key=f"edit_{entity_type}_{index}", use_container_width=True):
            if on_edit:
                on_edit(index)
            else:
                st.session_state[f'edit_{entity_type}_index'] = index
                st.rerun()

    with sub_col2:
        if st.button("🗑️ Apagar", key=f"delete_{entity_type}_{index}", use_container_width=True):
            if on_delete:
                on_delete(index)
            else:
                st.session_state[f'delete_{entity_type}_index'] = index
                st.rerun()


def render_edit_form(entity_type: str,
                     fields: Dict[str, Dict[str, Any]],
                     current_data: Dict[str, Any],
                     on_save: Callable) -> None:
    """Renderiza um formulário de edição padronizado."""
    entity_name = current_data.get('Nome', current_data.get('Nome Completo', 'Item'))
    st.subheader(f"Editar {entity_type}")

    with st.form(f"form_editar_{entity_type}"):
        form_data = {}

        if 'layout' in fields and fields['layout'] == 'columns':
            col1, col2 = st.columns(2)

            left_fields = fields.get('left', [])
            right_fields = fields.get('right', [])

            with col1:
                for field_config in left_fields:
                    form_data.update(_render_form_field(field_config, current_data))

            with col2:
                for field_config in right_fields:
                    form_data.update(_render_form_field(field_config, current_data))
        else:
            for field_config in fields.get('fields', []):
                form_data.update(_render_form_field(field_config, current_data))

        submit_label = fields.get('submit_label', "Guardar alterações")
        if st.form_submit_button(submit_label):
            if on_save(form_data):
                st.success(f"{entity_type.title()} '{entity_name}' atualizado com sucesso!")
                st.session_state[f'edit_{entity_type}_index'] = None
                st.rerun()


def _render_form_field(field_config: Dict[str, Any],
                      current_data: Dict[str, Any]) -> Dict[str, Any]:
    """Renderiza um campo individual do formulário."""
    field_name = field_config['name']
    field_type = field_config.get('type', 'text_input')
    label = field_config['label']
    required = field_config.get('required', False)
    value = current_data.get(field_name, field_config.get('default', ''))

    if field_type == 'text_input':
        return {field_name: st.text_input(label, value=value)}
    elif field_type == 'selectbox':
        options = field_config.get('options', [])
        try:
            index = options.index(value) if value in options else 0
        except (ValueError, TypeError):
            index = 0
        return {field_name: st.selectbox(label, options, index=index)}
    elif field_type == 'text_area':
        return {field_name: st.text_area(label, value=value)}
    elif field_type == 'number_input':
        min_val = field_config.get('min_value', 0.0)
        max_val = field_config.get('max_value', 1000.0)
        step = field_config.get('step', 1.0)
        return {field_name: st.number_input(label, value=float(value) if value else min_val,
                                             min_value=min_val, max_value=max_val, step=step)}
    elif field_type == 'date_input':
        min_date = field_config.get('min_value')
        max_date = field_config.get('max_value')
        return {field_name: st.date_input(label, value=value if value else None,
                                          min_value=min_date, max_value=max_date)}
    elif field_type == 'time_input':
        return {field_name: st.time_input(label, value=value if value else None)}

    return {field_name: st.text_input(label, value=value)}


def render_confirmation_dialog(entity_type: str,
                              entity_name: str,
                              on_confirm: Callable,
                              on_cancel: Callable) -> None:
    """Renderiza um diálogo de confirmação padronizado."""
    st.warning(f"Tens a certeza que queres apagar o {entity_type}: {entity_name}?")

    col1, col2, _ = st.columns([1, 1, 5])

    with col1:
        if st.button("✅ Sim, apagar", key=f"confirm_delete_{entity_type}"):
            if on_confirm():
                st.success(f"{entity_type.title()} '{entity_name}' apagado com sucesso!")
            else:
                st.error(f"Erro ao apagar o {entity_type}.")

    with col2:
        if st.button("❌ Cancelar", key=f"cancel_delete_{entity_type}"):
            on_cancel()


# ===== PRE-DEFINED CONFIGURATIONS FOR ENTITIES =====

USER_FIELDS_CONFIG = {
    'layout': 'columns',
    'left': [
        {'name': 'Nome', 'type': 'text_input', 'label': 'Nome do utente', 'required': True},
        {'name': 'Contacto', 'type': 'text_input', 'label': 'Contacto telefónico', 'required': True},
        {'name': 'Contacto_telefónico_2', 'type': 'text_input', 'label': 'Contacto telefónico 2'}
    ],
    'right': [
        {'name': 'Morada', 'type': 'text_input', 'label': 'Morada', 'required': True},
        {'name': 'Codigo_Postal', 'type': 'text_input', 'label': 'Código Postal (XXXX-XXX)', 'required': True},
        {'name': 'Localidade', 'type': 'text_input', 'label': 'Localidade'},
        {'name': 'Estado', 'type': 'selectbox', 'label': 'Estado', 'options': ['Ativo', 'Inativo']}
    ],
    'submit_label': "Guardar alterações"
}

PROFESSOR_FIELDS_CONFIG = {
    'layout': 'columns',
    'left': [
        {'name': 'Nome Completo', 'type': 'text_input', 'label': 'Nome Completo', 'required': True},
        {'name': 'Telefone', 'type': 'text_input', 'label': 'Telefone', 'required': True},
        {'name': 'Email', 'type': 'text_input', 'label': 'Email'}
    ],
    'right': [
        {'name': 'NIB', 'type': 'text_input', 'label': 'NIB'},
        {'name': 'Valor Hora', 'type': 'number_input', 'label': 'Valor hora (€)', 'min_value': 0.0, 'step': 0.5},
        {'name': 'Observacoes', 'type': 'text_area', 'label': 'Observações'}
    ],
    'submit_label': "Guardar alterações"
}

TURMA_FIELDS_CONFIG = {
    'fields': [
        {'name': 'nome_turma', 'type': 'text_input', 'label': 'Nome da turma', 'required': True},
        {'name': 'disciplina', 'type': 'selectbox', 'label': 'Disciplina', 'options': [], 'required': True},
        {'name': 'professor', 'type': 'selectbox', 'label': 'Professor', 'options': [], 'required': True},
        {'name': 'sala', 'type': 'selectbox', 'label': 'Sala', 'options': SALA_OPCOES},
        {'name': 'dia_semana', 'type': 'selectbox', 'label': 'Dia da semana', 'options': DIAS_SEMANA, 'required': True},
        {'name': 'hora_inicio', 'type': 'time_input', 'label': 'Hora de início', 'required': True},
        {'name': 'hora_fim', 'type': 'time_input', 'label': 'Hora de fim', 'required': True},
        {'name': 'nivel', 'type': 'selectbox', 'label': 'Nível', 'options': NIVEL_OPCOES},
        {'name': 'vagas', 'type': 'number_input', 'label': 'Número de vagas', 'min_value': 1, 'max_value': 50},
        {'name': 'estado', 'type': 'selectbox', 'label': 'Estado', 'options': ESTADO_OPCOES},
        {'name': 'observacoes', 'type': 'text_area', 'label': 'Observações'}
    ],
    'submit_label': "Guardar alterações"
}


# ===== CONVENIENCE FUNCTIONS =====

def render_user_edit_form(current_data: Dict[str, Any],
                         on_save: Callable) -> None:
    """Conveniência para formulário de edição de utente."""
    render_edit_form("utente", USER_FIELDS_CONFIG, current_data, on_save)


def render_professor_edit_form(current_data: Dict[str, Any],
                              on_save: Callable) -> None:
    """Conveniência para formulário de edição de professor."""
    render_edit_form("professor", PROFESSOR_FIELDS_CONFIG, current_data, on_save)


def render_turma_edit_form(current_data: Dict[str, Any],
                          on_save: Callable) -> None:
    """Conveniência para formulário de edição de turma."""
    render_edit_form("turma", TURMA_FIELDS_CONFIG, current_data, on_save)


# ===== DISPLAY COMPONENTS =====

def render_data_display_card(title: str,
                           data: Dict[str, Any],
                           field_mapping: Dict[str, str],
                           key_prefix: str = "display") -> None:
    """Renderiza um card padronizado para exibição de dados."""
    with st.expander(title):
        for field_key, field_label in field_mapping.items():
            if field_key in data and data[field_key]:
                value = data[field_key]

                # Formatação específica por campo
                if field_label.lower().startswith('valor hora') or field_label.lower().startswith('hora'):
                    formatted_value = format_currency(value)
                elif field_label.lower().startswith('nível') or field_label.lower().startswith('estado'):
                    formatted_value = value.title()
                elif field_label.lower().startswith('data'):
                    formatted_value = format_date_for_display(value)
                else:
                    formatted_value = str(value)

                st.text_input(field_label, value=formatted_value,
                             key=f"{key_prefix}_{field_key}", disabled=True)


def render_search_and_filter(search_placeholder: str = "Pesquisar...",
                           filter_dict: Optional[Dict[str, Any]] = None) -> str:
    """Renderiza componente de pesquisa e filtros padronizados."""
    col_search, *filter_cols = st.columns([2] + [1] * len(filter_dict) if filter_dict else [1])

    with col_search:
        search_text = st.text_input(search_placeholder, key="search_input")

    return search_text


def render_loading_indicator(message: str = "A processar dados..."):
    """Renderiza um indicador de carregamento padronizado."""
    with st.spinner(message):
        pass


def render_success_message(message: str, duration: int = 3):
    """Renderiza uma mensagem de sucesso temporária."""
    success_placeholder = st.empty()
    success_placeholder.success(message)

    if duration > 0:
        import time
        time.sleep(duration)
        success_placeholder.empty()


def render_error_message(message: str, errors: Optional[List[str]] = None):
    """Renderiza uma mensagem de erro com detalhes."""
    st.error(message)
    if errors:
        st.error("**Detalhes dos erros:**")
        for error in errors:
            st.error(f"• {error}")


def render_info_message(message: str, icon: str = "ℹ️"):
    """Renderiza uma mensagem informativa com ícone."""
    st.info(f"{icon} {message}")


def render_metric_card(title: str,
                      value: Any,
                      category: str = "info",
                      help_text: Optional[str] = None):
    """Renderiza um card métrico padronizado."""
    if help_text:
        st.metric(label=title, value=str(value), help=help_text)
    else:
        st.metric(label=title, value=str(value))
