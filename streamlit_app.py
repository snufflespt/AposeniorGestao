import streamlit as st

st.set_page_config(page_title="Gestão IPSS", page_icon="🧭", layout="wide")

st.title("Gestão IPSS")
st.write("Olá, Nuno! 👋")

st.divider()

st.subheader("Adicionar utente (teste)")

# Formulário simples
with st.form("form_utente"):
    nome = st.text_input("Nome do utente")
    contacto = st.text_input("Contacto")
    submit = st.form_submit_button("Guardar")

# Mostrar resultado
if submit:
    st.success(f"Utente '{nome}' com contacto '{contacto}' adicionado (teste).")
