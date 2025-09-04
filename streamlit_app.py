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

    st.dataframe(df_filtrado, use_container_width=True)

else:
    st.info("Ainda não existem utentes registados.")
