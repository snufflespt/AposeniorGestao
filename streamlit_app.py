import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# Lê as credenciais do secrets
creds_dict = st.secrets["google_service_account"]

# Define o escopo de permissões
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Cria as credenciais a partir do dicionário
creds = Credentials.from_service_account_info(creds_dict, scopes=scope)

# Autoriza o cliente
client = gspread.authorize(creds)

# Abre o ficheiro e a folha
sheet = client.open("Base_IPSS").worksheet("Utentes")

st.set_page_config(page_title="Gestão IPSS", page_icon="🧭", layout="wide")
st.title("Gestão IPSS")
st.write("Olá, Nuno! 👋")

st.divider()
st.subheader("Adicionar utente")

# Formulário para adicionar utente
with st.form("form_utente"):
    nome = st.text_input("Nome do utente")
    contacto = st.text_input("Contacto")
    submit = st.form_submit_button("Guardar")

if submit:
    if nome.strip() == "" or contacto.strip() == "":
        st.error("Por favor, preencha todos os campos antes de guardar.")
    else:
        sheet.append_row([nome, contacto])
        st.success(f"Utente '{nome}' com contacto '{contacto}' adicionado ao Google Sheets!")

# Inicio da tabela de pesquisa/edicao e remover
st.divider()
st.subheader("Lista de utentes")

# Ler todos os dados da folha
dados = sheet.get_all_records()

if dados:
    df = pd.DataFrame(dados)

    # Campo de pesquisa
    pesquisa = st.text_input("Pesquisar utente por nome ou contacto:")

    if pesquisa:
        df_filtrado = df[df.apply(lambda row: pesquisa.lower() in row.astype(str).str.lower().to_string(), axis=1)]
    else:
        df_filtrado = df

    # Mostrar tabela com botões
    for i, row in df_filtrado.iterrows():
        col1, col2, col3 = st.columns([3, 2, 2])
        col1.write(f"**{row['Nome']}** — {row['Contacto']}")
        if col2.button("✏️ Editar", key=f"edit_{i}"):
            st.session_state['edit_index'] = i
        if col3.button("🗑️ Apagar", key=f"delete_{i}"):
            st.session_state['delete_index'] = i

    # Confirmação de apagar
    if 'delete_index' in st.session_state:
        idx = st.session_state['delete_index']
        st.warning(f"Tens a certeza que queres apagar o utente: {df.iloc[idx]['Nome']}?")
        col_conf1, col_conf2 = st.columns(2)
        if col_conf1.button("✅ Sim, apagar"):
            sheet.delete_rows(idx+2)  # +2 por causa do cabeçalho
            del st.session_state['delete_index']
            st.rerun()
        if col_conf2.button("❌ Cancelar"):
            del st.session_state['delete_index']
            st.rerun()

    # Modo edição
    if 'edit_index' in st.session_state:
        idx = st.session_state['edit_index']
        st.subheader("Editar utente")
        with st.form("form_editar"):
            novo_nome = st.text_input("Nome do utente", value=df.iloc[idx]['Nome'])
            novo_contacto = st.text_input("Contacto", value=df.iloc[idx]['Contacto'])
            guardar = st.form_submit_button("Guardar alterações")
        if guardar:
            sheet.update_cell(idx+2, 1, novo_nome)     # Coluna 1 = Nome
            sheet.update_cell(idx+2, 2, novo_contacto) # Coluna 2 = Contacto
            del st.session_state['edit_index']
            st.rerun()

else:
    st.info("Ainda não existem utentes registados.")
