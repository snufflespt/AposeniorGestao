import streamlit as st

st.set_page_config(page_title="Gestão IPSS", page_icon="🧭", layout="wide")

st.title("Gestão IPSS")
st.write("Olá, Nuno! 👋")
st.divider()

with st.sidebar:
    st.header("Menu")
    st.write("Por enquanto, só um olá. Vamos passo a passo.")

st.success("A app está a funcionar. Próximo: ligar ao Google Sheets.")
