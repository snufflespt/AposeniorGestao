import streamlit as st
import hashlib
from utils.sheets import get_worksheet

def check_credentials(username, password):
    """Verifica as credenciais contra a worksheet 'Credenciais'."""
    try:
        sheet = get_worksheet("Credenciais")
        users = sheet.get_all_records()
        
        for user in users:
            if user['username'] == username:
                # Verificar a password com hash
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                if user['password_hash'] == hashed_password:
                    st.session_state['username'] = user['username'] # Guardar nome de utilizador
                    return True
        return False
    except Exception as e:
        st.error(f"Não foi possível verificar as credenciais. Verifique a folha 'Credenciais'. Erro: {e}")
        return False

def login_form():
    """Mostra o formulário de login e gere a lógica de autenticação."""
    st.image("imagens/logo.png", width=200)
    st.title("Gestão IPSS - Login")
    with st.form("login_form"):
        username = st.text_input("Utilizador")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Entrar")

        if submitted:
            if check_credentials(username, password):
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Utilizador ou password incorreta.")

def show_login():
    """Função principal para mostrar o login ou a app."""
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        login_form()
        st.stop()
