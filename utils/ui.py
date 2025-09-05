import streamlit as st
import base64

def configurar_pagina(titulo, icone="🧭"):
    """Configura título, ícone e layout da página."""
    st.set_page_config(page_title=titulo, page_icon=icone, layout="wide")
    aplicar_estilos()
    st.title(f"{icone} {titulo}")

def imagem_base64(caminho):
    with open(caminho, "rb") as f:
        dados = f.read()
    return base64.b64encode(dados).decode()

def aplicar_estilos():
    mascote_b64 = imagem_base64("imagens/mascote.png")
    st.markdown(
        f"""
        <style>
        html, body, [class*="css"] {{
            font-family: 'Segoe UI', sans-serif;
            color: #2E2E2E;
        }}

        div.stButton > button:first-child {{
            background-color: #F26A21;
            color: white;
            border-radius: 6px;
            padding: 0.5em 1em;
            font-size: 1rem;
            border: none;
        }}
        div.stButton > button:hover {{
            background-color: #E94E1B;
            color: white;
        }}

        h1, h2, h3 {{
            color: #F26A21;
        }}

        .stTextInput > div > div > input,
        .stSelectbox > div > div > select,
        textarea {{
            border-radius: 5px;
            border: 1px solid #ccc;
            color: #2E2E2E;
        }}

        section[data-testid="stSidebar"] {{
            background-color: #f9f9f9;
            font-size: 1.15rem;
        }}
        section[data-testid="stSidebar"] * {{
            color: #2E2E2E !important;
        }}

        section[data-testid="stSidebar"] [role="radio"][aria-checked="true"] {{
            background-color: #F26A21;
            border-radius: 5px;
            padding: 0.3em;
            font-weight: bold;
            color: white !important;
        }}

        /* Tabs */
        button[role="tab"] {{
            font-size: 1rem;
            color: #F26A21;
            transition: all 0.2s ease-in-out;
        }}
        button[role="tab"][aria-selected="true"] {{
            font-weight: bold !important;
            font-size: 1.25rem !important;
            border-bottom: 3px solid #F26A21 !important;
        }}

        [data-testid="stAppViewContainer"] {{
            background: linear-gradient(135deg, #f0e9e4 0%, #e6d9d0 100%);
            background-attachment: fixed;
        }}

        [data-testid="stAppViewContainer"]::after {{
            content: "";
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 250px;
            height: 250px;
            background-image: url("data:image/png;base64,{mascote_b64}");
            background-size: contain;
            background-repeat: no-repeat;
            opacity: 0.35;
            pointer-events: none;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )






def titulo_secao(texto, icone="📌"):
    """Mostra um título de secção com divisor."""
    st.markdown(f"### {icone} {texto}")
    st.divider()
