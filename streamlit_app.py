import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

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

with st.form("form_utente"):
    nome = st.text_input("Nome do utente")
    contacto = st.text_input("Contacto")
    submit = st.form_submit_button("Guardar")

if submit:
    sheet.append_row([nome, contacto])
    st.success(f"Utente '{nome}' com contacto '{contacto}' adicionado ao Google Sheets!")
