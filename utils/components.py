"""
Biblioteca de componentes reutilizáveis para a aplicação Streamlit
Centraliza lógica comum para exibição de dados e interações
"""

import streamlit as st
from typing import Dict, Any, Optional, Callable


def render_user_card(user_data: Dict[str, Any], index: int, on_edit: Optional[Callable] = None, on_delete: Optional[Callable] = None) -> None:
    """
    Renderiza um card de utente com informações e botões de ação

    Args:
        user_data: Dicionário com dados do utente
        index: Índice do utente na lista
        on_edit: Callback para ação de editar
        on_delete: Callback para ação de apagar
    """
    nome = user_data.get('Nome', '')
    contacto = user_data.get('Contacto', '')
    morada = user_data.get('Morada', '')
    estado = user_data.get('Estado', '')

    # Container para agrupar elementos
    with st.container():
        # Layout em colunas para informação e botões
        col_info, col_actions = st.columns([4, 1])

        with col_info:
            # Nome e contacto
            st.markdown(f"**{nome}** — {contacto}")

            # Morada se existir
            if morada:
                st.markdown(f"🏠 {morada}")

            # Status badge colorido
            if estado == 'Ativo':
                st.markdown('<span style="background-color: #d4edda; color: #155724; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">● ATIVO</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span style="background-color: #f8d7da; color: #721c24; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">● INATIVO</span>', unsafe_allow_html=True)

        with col_actions:
            render_action_buttons(index, on_edit, on_delete)

        st.divider()


def render_action_buttons(index: int, on_edit: Optional[Callable] = None, on_delete: Optional[Callable] = None, entity_type: str = "item") -> None:
    """
    Renderiza botões de ação padronizados (Editar/Apagar)

    Args:
        index: Índice do item para chaves únicas
        on_edit: Função callback para editar
        on_delete: Função callback para apagar
        entity_type: Tipo de entidade (para chaves de session_state)
    """
    # Sub-colunas para os dois botões
    sub_col1, sub_col2 = st.columns(2)

    with sub_col1:
        if st.button("✏️ Editar", key=f"edit_{entity_type}_{index}", use_container_width=True):
            if on_edit:
                on_edit(index)
            else:
                # Fallback padrão
                st.session_state[f'edit_{entity_type}_index'] = index
                st.rerun()

    with sub_col2:
        if st.button("🗑️ Apagar", key=f"delete_{entity_type}_{index}", use_container_width=True):
            if on_delete:
                on_delete(index)
            else:
                # Fallback padrão
                st.session_state[f'delete_{entity_type}_index'] = index
                st.rerun()


def render_edit_form(entity_type: str, fields: Dict[str, Dict[str, Any]], current_data: Dict[str, Any], on_save: Callable) -> None:
    """
    Renderiza um formulário de edição padronizado

    Args:
        entity_type: Tipo da entidade (ex: "utente", "professor")
        fields: Configuração dos campos do formulário
        current_data: Dados atuais para preencher o formulário
        on_save: Função callback para salvar alterações
    """
    entity_name = current_data.get('Nome', current_data.get('Nome do Professor', 'Item'))

    st.subheader(f"Editar {entity_type}")

    with st.form(f"form_editar_{entity_type}"):
        form_data = {}

        # Criar campos baseado na configuração
        if 'layout' in fields and fields['layout'] == 'columns':
            # Layout em colunas
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
            # Campos individuais
            for field_config in fields.get('fields', []):
                form_data.update(_render_form_field(field_config, current_data))

        # Botão de salvar
        submit_label = fields.get('submit_label', f"Guardar alterações")
        if st.form_submit_button(submit_label):
            if on_save(form_data):
                st.success(f"{entity_type.title()} '{entity_name}' atualizado com sucesso!")
                # Limpar estado de edição
                if f'edit_{entity_type}_index' in st.session_state:
                    del st.session_state[f'edit_{entity_type}_index']
                st.rerun()


def _render_form_field(field_config: Dict[str, Any], current_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Renderiza um campo individual do formulário

    Args:
        field_config: Configuração do campo
        current_data: Dados atuais

    Returns:
        Dict com dados do campo
    """
    field_name = field_config['name']
    field_type = field_config.get('type', 'text_input')
    label = field_config['label']
    required = field_config.get('required', False)
    value = current_data.get(field_name, field_config.get('default', ''))

    if field_type == 'text_input':
        return {field_name: st.text_input(label, value=value)}
    elif field_type == 'selectbox':
        options = field_config.get('options', [])
        # Encontrar índice do valor atual
        try:
            index = options.index(value) if value in options else 0
        except (ValueError, TypeError):
            index = 0
        return {field_name: st.selectbox(label, options, index=index)}
    elif field_type == 'text_area':
        return {field_name: st.text_area(label, value=value)}

    return {}


def render_confirmation_dialog(entity_type: str, entity_name: str, on_confirm: Callable, on_cancel: Callable) -> None:
    """
    Renderiza um diálogo de confirmação padronizado

    Args:
        entity_type: Tipo da entidade
        entity_name: Nome da entidade
        on_confirm: Callback para confirmação
        on_cancel: Callback para cancelamento
    """
    st.warning(f"Tens a certeza que queres apagar o {entity_type}: {entity_name}?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Sim, apagar"):
            if on_confirm():
                st.success(f"{entity_type.title()} '{entity_name}' apagado com sucesso!")
            else:
                st.error("Erro ao apagar o item.")

    with col2:
        if st.button("❌ Cancelar"):
            on_cancel()


# Configurações pré-definidas para entidades comuns
USER_FIELDS_CONFIG = {
    'layout': 'columns',
    'left': [
        {'name': 'Nome', 'type': 'text_input', 'label': 'Nome do utente', 'required': True},
        {'name': 'Contacto', 'type': 'text_input', 'label': 'Contacto', 'required': True}
    ],
    'right': [
        {'name': 'Morada', 'type': 'text_input', 'label': 'Morada'},
        {'name': 'Estado', 'type': 'selectbox', 'label': 'Estado', 'options': ['Ativo', 'Inativo']}
    ]
}

def render_user_edit_form(current_data: Dict[str, Any], on_save: Callable) -> None:
    """Conveniência para formulário de edição de utente"""
    render_edit_form("utente", USER_FIELDS_CONFIG, current_data, on_save)
