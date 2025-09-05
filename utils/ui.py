import streamlit as st
import base64

def configurar_pagina(titulo, icone="🧭"):
    """Configura título, ícone e layout da página."""
    st.set_page_config(page_title=titulo, page_icon=icone, layout="wide")
    aplicar_estilos()
    st.title(f"{icone} {titulo}")

def imagem_base64(caminho):
    """Converte imagem para base64 para usar no CSS."""
    with open(caminho, "rb") as f:
        dados = f.read()
    return base64.b64encode(dados).decode()

def aplicar_estilos():
    mascote_b64 = imagem_base64("imagens/mascote.png")
    st.markdown(
        f"""
        <style>
        /* Fonte global */
        html, body, [class*="css"] {{
            font-family: 'Segoe UI', sans-serif;
            color: #2E2E2E;
        }}

        /* Botões */
        div.stButton > button:first-child {{
            background-color: #F26A21;
            color: white;
            border-radius: 6px;
            padding: 0.5em 1em;
            font-size: 1rem;
            border: none;
            transition: all 0.2s ease-in-out;
        }}
        div.stButton > button:hover {{
            background-color: #E94E1B;
            transform: scale(1.10);
        }}

        /* Alinhar verticalmente colunas e igualar altura */
        div[data-testid="column"] > div {{
            display: flex;
            align-items: center;
        }}
        
        /* Ajustar altura dos botões para igualar ao texto */
        div.stButton > button {{
            padding-top: 0.6rem;
            padding-bottom: 0.6rem;
        }}

        
        /* Linha de texto: uma só linha com reticências */
        .linha-texto {{
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            line-height: 1.2rem; /* altura baixa e consistente */
        }}
        
        /* Botões lado a lado mais compactos */
        div.stButton > button {{
            padding: 0.35rem 0.5rem;
        }}
        
        /* Fallback: centralizar verticalmente colunas de ações mesmo sem vertical_alignment */
        div[data-testid="column"] > div {{
            display: flex;
            align-items: center;
        }}

        /* Títulos */
        h1, h2, h3 {{
            color: #F26A21;
        }}

        /* Aproximar botões de ação */
        div.stButton {{
        margin-right: 0.2rem;
        margin-left: 0.2rem;
        }}


        /* Campos de input */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > select,
        textarea {{
            border-radius: 5px;
            border: 1px solid #ccc;
            color: #2E2E2E;
        }}

        /* MENU LATERAL - branco */
        section[data-testid="stSidebar"] {{
            background-color: white;
            font-size: 1.15rem;
        }}
        section[data-testid="stSidebar"] * {{
            color: #2E2E2E !important;
        }}

        /* LOGO - centralizado e sem rectângulo branco */
        section[data-testid="stSidebar"] img {{
            display: block;
            margin: 0 auto;
            background-color: #3a3a3a; /* fundo escuro */
            padding: 8px;
            border-radius: 8px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.2);
        }}
        section[data-testid="stSidebar"] [data-testid="stImage"] {{
            background: none !important;
            padding: 0 !important;
        }}

        /* OPÇÃO ATIVA NO MENU LATERAL */
        section[data-testid="stSidebar"] [role="radio"][aria-checked="true"] > div {{
            background-color: #F26A21 !important;
            border-radius: 5px;
            padding: 0.4em;
            font-weight: bold !important;
            font-size: 1.1rem !important;
            color: white !important;
            transition: all 0.2s ease-in-out;
        }}

        /* Tabs */
        button[role="tab"] {{
            font-size: 1rem;
            color: #F26A21;
            transition: all 0.2s ease-in-out;
        }}
        button[role="tab"][aria-selected="true"] {{
            font-weight: bold !important;
            font-size: 1.10rem !important;
            border-bottom: 6px solid #F26A21 !important;
            transform: scale(1.05);
        }}

        /* Fundo geral */
        [data-testid="stAppViewContainer"] {{
            background: linear-gradient(135deg, #e8e1da 0%, #d8ccc2 100%);
            background-attachment: fixed;
        }}

        /* Glassmorphism no conteúdo */
        [data-testid="stVerticalBlock"] > div:first-child {{
            background: rgba(255, 255, 255, 0.65);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            transition: transform 0.2s ease-in-out;
        }}
        [data-testid="stVerticalBlock"] > div:first-child:hover {{
            transform: translateY(-2px);
        }}

        /* Marca de água da mascote */
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
            opacity: 0.25;
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
