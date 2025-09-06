import streamlit as st
import pandas as pd
import time
from utils.sheets import get_worksheet
from utils.ui import configurar_pagina, titulo_secao
from utils.components import (
    render_user_card,
    render_confirmation_dialog
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
                df_filtrado = df[df.apply(lambda row: pesquisa.lower() in row.astype(str).str.lower().to_string(), axis=1)]
            else:
                df_filtrado = df

            # Renderizar lista de utentes usando componentes reutilizáveis
            for i, row in df_filtrado.iterrows():
                render_user_card(dict(row), i)



            # Diálogo de confirmação usando componente reutilizável
            if 'delete_index' in st.session_state:
                idx = st.session_state['delete_index']
                entity_name = df.iloc[idx]['Nome']

                def confirm_delete():
                    try:
                        sheet.delete_rows(idx + 2)
                        return True
                    except Exception as e:
                        st.error(f"Erro ao apagar utente: {str(e)}")
                        return False

                def cancel_delete():
                    del st.session_state['delete_index']

                render_confirmation_dialog('utente', entity_name, confirm_delete, cancel_delete)

            if 'edit_index' in st.session_state:
                idx = st.session_state['edit_index']
                st.subheader("Editar utente")

                with st.form("form_editar"):
                    novo_nome = st.text_input("Nome do utente", value=df.iloc[idx]['Nome'])
                    novo_contacto = st.text_input("Contacto", value=df.iloc[idx]['Contacto'])
                    nova_morada = st.text_input("Morada", value=df.iloc[idx].get('Morada', ''))
                    novo_estado = st.selectbox("Estado", ["Ativo", "Inativo"],
                                              index=["Ativo", "Inativo"].index(df.iloc[idx].get('Estado', 'Ativo')))

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
        # Atualizar cada campo
        sheet.update_cell(index + 2, 1, dados.get('Nome', ''))
        sheet.update_cell(index + 2, 2, dados.get('Contacto', ''))
        sheet.update_cell(index + 2, 3, dados.get('Morada', ''))
        sheet.update_cell(index + 2, 4, dados.get('Estado', 'Ativo'))
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
