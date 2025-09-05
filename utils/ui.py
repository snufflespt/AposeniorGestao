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
        /* Fonte global */
        html, body, [class*="css"] {
            font-family: 'Segoe UI', sans-serif;
            color: #2E2E2E;
        }

        /* Botões */
        div.stButton > button:first-child {
            background-color: #F26A21; /* laranja principal */
            color: white;
            border-radius: 6px;
            padding: 0.5em 1em;
            font-size: 1rem;
            border: none;
        }
        div.stButton > button:hover {
            background-color: #E94E1B; /* vermelho-alaranjado */
            color: white;
        }

        /* Títulos */
        h1, h2, h3 {
            color: #F26A21; /* cor principal */
        }

        /* Campos de input */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > select,
        textarea {
            border-radius: 5px;
            border: 1px solid #ccc;
        }

        /* MENU LATERAL */
        section[data-testid="stSidebar"] {
            background-color: #F5F5F5; /* fundo suave */
            font-size: 1.15rem;
        }
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            font-size: 1.15rem;
        }
        section[data-testid="stSidebar"] .css-1v3fvcr,
        section[data-testid="stSidebar"] .css-1d391kg {
            font-size: 1.15rem !important;
            line-height: 1.6;
        }

        /* Destacar opção ativa no menu lateral */
        section[data-testid="stSidebar"] [role="radio"][aria-checked="true"] {
            background-color: #F9A82533; /* amarelo dourado translúcido */
            border-radius: 5px;
            padding: 0.3em;
            font-weight: bold;
            color: #E94E1B;
        }

        /* Tabs */
        .stTabs [data-baseweb="tab"] {
            font-size: 1rem;
            color: #F26A21;
        }
        .stTabs [aria-selected="true"] {
            font-weight: bold;
            border-bottom: 3px solid #F26A21;
        }
        </style>
        """,
        unsafe_allow_html=True
    )



def titulo_secao(texto, icone="📌"):
    """Mostra um título de secção com divisor."""
    st.markdown(f"### {icone} {texto}")
    st.divider()
