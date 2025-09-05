import streamlit as st

def configurar_pagina(titulo, icone="🧭"):
    """Configura título, ícone e layout da página."""
    st.set_page_config(page_title=titulo, page_icon=icone, layout="wide")
    aplicar_estilos()
    st.title(f"{icone} {titulo}")

def aplicar_estilos():
    st.markdown(
        """
        <style>
        /* Botões */
        div.stButton > button:first-child {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 0.5em 1em;
            font-size: 1rem;
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

        /* MENU LATERAL - aumentar tamanho do texto e ícones */
        section[data-testid="stSidebar"] {
            font-size: 1.15rem;   /* aumenta tamanho do texto */
        }
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            font-size: 1.15rem;   /* aumenta tamanho do texto de markdown */
        }

        /* Ícones e labels do menu */
        section[data-testid="stSidebar"] .css-1v3fvcr, /* ícones */
        section[data-testid="stSidebar"] .css-1d391kg { /* labels */
            font-size: 1.15rem !important;
            line-height: 1.6;
        }

        /* Destacar opção ativa no menu lateral */
        section[data-testid="stSidebar"] .stRadio > label[data-baseweb="radio"] > div[role="radio"][aria-checked="true"] {
            background-color: #e6f2ff; /* fundo azul claro */
            border-radius: 5px;
            padding: 0.3em;
            font-weight: bold;
            color: #004080;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def titulo_secao(texto, icone="📌"):
    """Mostra um título de secção com divisor."""
    st.markdown(f"### {icone} {texto}")
    st.divider()
