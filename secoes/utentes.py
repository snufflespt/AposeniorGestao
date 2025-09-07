import streamlit as st
import pandas as pd
import time
from utils.sheets import get_worksheet
from utils.ui import configurar_pagina, titulo_secao
from utils.components import (
    render_confirmation_dialog, render_action_buttons

)

def mostrar_pagina():
    configurar_pagina("Gestão de Utentes", "🧍")

    sheet = get_worksheet("Utentes")

    # Criar tabs
    tab_adicionar, tab_gerir = st.tabs(["➕ Adicionar utente", "📋 Gerir utentes"])

    with tab_adicionar:
        titulo_secao("Adicionar novo utente", "➕")
        with st.form("form_utente"):
            col1, col2 = st.columns(2)
            with col1:
                nome = st.text_input("Nome do utente")
                contacto = st.text_input("Contacto")
            with col2:
                morada = st.text_input("Morada")
                estado = st.selectbox("Estado", ["Ativo", "Inativo"])
            submit = st.form_submit_button("Guardar")

        if submit:
            if nome.strip() == "" or contacto.strip() == "":
                st.error("Por favor, preencha os campos obrigatórios.")
            else:
                if adicionar_utente(sheet, nome, contacto, morada, estado):
                    st.success(f"Utente '{nome}' adicionado com sucesso!")
                    st.rerun()

    with tab_gerir:
        st.markdown("### Lista de utentes")

        dados = sheet.get_all_records()

        if dados:
            df = pd.DataFrame(dados)
            pesquisa = st.text_input("Pesquisar utente por qualquer campo:")

            if pesquisa:
                df_filtrado = df[df.apply(lambda row: any(pesquisa.lower() in str(x).lower() for x in row), axis=1)]
            else:
                df_filtrado = df

            # Renderizar lista de utentes com cartões expansíveis
            for i, row in df_filtrado.iterrows():
                with st.expander(f"**{row.get('Nome', '')}**"):
                    card_col, actions_col = st.columns([4, 1])

                    with card_col:
                        with st.container(border=True):
                            st.markdown(f"**Contacto:** {row.get('Contacto', 'N/A')}")
                            st.markdown(f"**Morada:** {row.get('Morada', 'N/A')}")
                            st.markdown(f"**Estado:** {row.get('Estado', 'N/A')}")

                    with actions_col:
                        # Usar o índice do DataFrame (i) que corresponde à linha original
                        if st.button("✏️ Editar", key=f"edit_utente_{i}", use_container_width=True):
                            st.session_state['edit_index'] = i
                            st.rerun()

                        if st.button("🗑️ Apagar", key=f"delete_utente_{i}", use_container_width=True):
                            st.session_state['delete_index'] = i
                            st.rerun()

            # --- Diálogos de Ação (Apagar / Editar) ---

            # Diálogo de confirmação para apagar
            if 'delete_index' in st.session_state:
                idx = st.session_state['delete_index']
                # Usar o dataframe original (df) para obter os dados do utente pelo índice
                entity_name = df.loc[idx, 'Nome']

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

            if 'edit_index' in st.session_state:
                idx = st.session_state['edit_index']
                utente_atual = df.loc[idx]
                st.subheader(f"Editar utente: {utente_atual['Nome']}")

                with st.form("form_editar"):
                    novo_nome = st.text_input("Nome do utente", value=utente_atual['Nome'])
                    novo_contacto = st.text_input("Contacto", value=utente_atual['Contacto'])
                    nova_morada = st.text_input("Morada", value=utente_atual.get('Morada', ''))
                    
                    estado_options = ["Ativo", "Inativo"]
                    estado_atual = utente_atual.get('Estado', 'Ativo')
                    # Prevenir erro se estado_atual não estiver nas opções
                    estado_index = estado_options.index(estado_atual) if estado_atual in estado_options else 0
                    novo_estado = st.selectbox("Estado", estado_options, index=estado_index)

                    if st.form_submit_button("Guardar alterações"):
                        novos_dados = {
                            'Nome': novo_nome,
                            'Contacto': novo_contacto,
                            'Morada': nova_morada,
                            'Estado': novo_estado
                        }

                        if atualizar_utente(sheet, idx, novos_dados):
                            st.success(f"Utente '{novo_nome}' atualizado com sucesso!")
                            del st.session_state['edit_index']
                            time.sleep(0.5)  # Pequena pausa para mostrar mensagem
                            st.rerun()
        else:
            st.info("Ainda não existem utentes registados.")


# Funções auxiliares para operações CRUD
def adicionar_utente(sheet, nome: str, contacto: str, morada: str = "", estado: str = "Ativo") -> bool:
    """
    Adiciona um novo utente à planilha

    Args:
        sheet: Planilha do Google Sheets
        nome: Nome do utente
        contacto: Contacto do utente
        morada: Morada do utente (opcional)
        estado: Estado do utente

    Returns:
        True se adicionado com sucesso, False caso contrário
    """
    try:
        sheet.append_row([nome, contacto, morada, estado])
        return True
    except Exception as e:
        st.error(f"Erro ao adicionar utente: {str(e)}")
        return False

def atualizar_utente(sheet, index: int, dados: dict) -> bool:
    """
    Atualiza os dados de um utente na planilha

    Args:
        sheet: Planilha do Google Sheets
        index: Índice do utente na planilha
        dados: Dicionário com novos dados

    Returns:
        True se atualizado com sucesso, False caso contrário
    """
    try:
        # Criar lista de valores para atualizar a linha
        values = [
            dados.get('Nome', ''),
            dados.get('Contacto', ''),
            dados.get('Morada', ''),
            dados.get('Estado', 'Ativo')
        ]
        # Atualizar a linha na planilha
        sheet.update(f'A{index + 2}:D{index + 2}', [values])
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
