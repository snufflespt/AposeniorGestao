import streamlit as st

def configurar_pagina(titulo, icone="🧭"):
    """Configura título, ícone e layout da página."""
    st.set_page_config(page_title=titulo, page_icon=icone, layout="wide")
    aplicar_estilos()
    st.title(f"{icone} {titulo}")

def aplicar_estilos():
    """Aplica CSS global para toda a aplicação."""
    st.markdown(
        """
        <style>
        /* Botões */
        div.stButton > button:first-child {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 0.5em 1em;
        }
        div.stButton > button:hover {
            background-color: #45a049;
            color: white;
        }
        /* Títulos */
        h1, h2, h3 {
            color: #2E4053;
        }
        /* Campos de input */
        .stTextInput > div > div > input {
            border-radius: 5px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def titulo_secao(texto, icone="📌"):
    """Mostra um título de secção com divisor."""
    st.markdown(f"### {icone} {texto}")
    st.divider()
