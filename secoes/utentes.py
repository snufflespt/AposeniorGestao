import streamlit as st
import pandas as pd
import time
from utils.sheets import get_worksheet
from utils.ui import configurar_pagina, titulo_secao
from utils.components import (
    render_confirmation_dialog, render_action_buttons

)

# Configuração da página com tema moderno
def configurar_tema():
    st.markdown("""
        <style>
            :root {
                --primary-color: #264653;
                --background-color: #f4f4f4;
                --text-color: #333333;
                --font-family: 'Arial', sans-serif;
            }
            body {
                background-color: var(--background-color);
                color: var(--text-color);
                font-family: var(--font-family);
            }
            .stApp {
                background-color: var(--background-color);
            }
            h1, h2, h3, h4, h5, h6 {
                color: var(--primary-color);
            }
            .css-10trblm { /* stTextInput, stNumberInput, stTextArea */
                background-color: white;
                border-radius: 5px;
                border: 1px solid #ccc;
                padding: 5px 10px;
            }
            .css-qrbaxs { /* stSelectbox */
                background-color: white;
                border-radius: 5px;
                border: 1px solid #ccc;
                padding: 5px 10px;
            }
            .css-1egviio { /* submit button */
                background-color: var(--primary-color);
                color: white;
                border-radius: 5px;
                padding: 5px 10px;
                border: none;
            }
            .css-1egviio:hover {
                background-color: #2a9d8f;
            }
        </style>
    """, unsafe_allow_html=True)


def mostrar_pagina():
    st.markdown("""
        <style>
        .user-card {
            background-color: #fff;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)


def mostrar_pagina():
    configurar_pagina("Gestão de Utentes", "🧍")
    configurar_tema()  # Aplicar o tema

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

            # Renderizar lista de utentes usando componentes reutilizáveis
            for i, row in df_filtrado.iterrows():
                col1, col2 = st.columns([4, 2])

                nome = row.get('Nome', '')
                contacto = row.get('Contacto', '')

                col1.write(f"**{nome}** — {contacto}")
                
                with col2:
                    btn_col1, btn_col2 = st.columns(2)
                    if btn_col1.button("✏️ Editar", key=f"edit_utente_{i}", use_container_width=True):
                        st.session_state['edit_utente_index'] = i
                    if btn_col2.button("🗑️ Apagar", key=f"delete_utente_{i}", use_container_width=True):
                        st.session_state['delete_utente_index'] = i

            if 'delete_utente_index' in st.session_state:
                idx = st.session_state['delete_utente_index']
                st.warning(f"Tens a certeza que queres apagar o utente: {df.iloc[idx]['Nome']}?")
                col_conf1, col_conf2 = st.columns(2)
                if col_conf1.button("✅ Sim, apagar"):
                    sheet.delete_rows(idx + 2)
                    del st.session_state['delete_utente_index']
                    st.rerun()
            # Diálogo de confirmação usando componente reutilizável
            if 'delete_index' in st.session_state:
                idx = st.session_state['delete_index']
                entity_name = df.iloc[idx['Nome']   ]   

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
