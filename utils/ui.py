import streamlit as st
import base64

def configurar_pagina(titulo, icone="🧭"):
    """Configura título, ícone e layout da página."""
    st.set_page_config(page_title=titulo, page_icon=icone, layout="wide")
    aplicar_estilos()
    # Título discreto (sem barra grande)
    st.markdown(f"### {icone} {titulo}")

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
        :root {{
            --color-bg: #1e1e1e; /* Fundo escuro */
            --color-sidebar-bg: #252526; /* Sidebar ligeiramente diferente */
            --color-text: #e0e0e0; /* Texto claro */
            --color-card: #2c2c2c; /* Fundo dos cards */
            --color-brand: #F26A21; /* Laranja Fénix */
            --color-brand-hover: #D9530A; /* Laranja mais escuro no hover */
            --color-border: #444444; /* Borda subtil */
            --font-family: 'Inter', 'Segoe UI', sans-serif;
            --radius: 10px;
            --fs-body: 15px;
            --shadow: 0 4px 12px rgba(0, 0, 0, 0.4); /* Sombra para tema escuro */
        }}

        /* --- CONFIGURAÇÕES GLOBAIS --- */
        
        html, body, [class*="css"] {{
            font-family: var(--font-family);
            background-color: var(--color-bg);
            color: var(--color-text);
            font-size: var(--fs-body);
        }}
        
        .block-container {{
            padding-top: 2rem !important;
        }}

        /* --- ESTILOS DE COMPONENTES --- */

        /* Botão Geral */
        [data-testid="stButton"] > button {{
            background-color: var(--color-brand);
            color: white;
            border: none;
            border-radius: var(--radius);
            padding: 0.6rem 1.2rem;
            font-size: 1rem;
            cursor: pointer;
            transition: background-color 0.2s ease, transform 0.2s ease;
        }}
        [data-testid="stButton"] > button:hover {{
            background-color: var(--color-brand-hover);
            transform: translateY(-2px);
        }}

        /* Inputs e TextAreas */
        [data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea, [data-testid="stSelectbox"] div[data-baseweb="select"] > div {{
            border: 1px solid var(--color-border);
            border-radius: var(--radius);
            background-color: #333333; /* Fundo escuro para inputs */
            color: var(--color-text);
        }}
        [data-testid="stTextInput"] input:disabled, [data-testid="stTextArea"] textarea:disabled {{
            -webkit-text-fill-color: #a0a0a0;
            color: #a0a0a0;
            background-color: #2a2a2a;
        }}

        /* Menu Lateral */
        [data-testid="stSidebar"] {{
            background-color: var(--color-sidebar-bg);
            border-right: 1px solid var(--color-border);
        }}
        
        /* Estilos para o streamlit-option-menu */
        [data-testid="stSidebar"] .nav-link {{
            font-size: 1rem;
            color: var(--color-text) !important; /* Cor do texto clara */
            border-radius: var(--radius);
            margin: 4px 0;
            transition: background-color 0.2s ease, color 0.2s ease;
        }}
        [data-testid="stSidebar"] .nav-link:hover {{
            background-color: rgba(242, 106, 33, 0.15);
            color: var(--color-brand) !important;
        }}
        [data-testid="stSidebar"] .nav-link-selected {{
            background-color: var(--color-brand) !important;
            color: white !important;
            font-weight: 600;
        }}
        [data-testid="stSidebar"] .nav-link-selected:hover {{
            background-color: var(--color-brand-hover) !important;
        }}

        /* Imagem do logo na sidebar */
        [data-testid="stSidebar"] [data-testid="stImage"] img {{
            padding: 0.5rem;
            border-radius: var(--radius);
        }}
        
        /* Abas (Tabs) */
        button[role="tab"] {{
            font-size: 1.05rem;
            border-radius: var(--radius) var(--radius) 0 0;
            color: var(--color-text);
        }}
        button[role="tab"][aria-selected="true"] {{
            font-weight: bold;
            background-color: var(--color-card);
            border-bottom: 3px solid var(--color-brand);
        }}

        /* Métricas no Dashboard */
        [data-testid="stMetric"] {{
            background-color: var(--color-card);
            border-radius: var(--radius);
            padding: 1.5rem;
            box-shadow: var(--shadow);
            border-left: 5px solid var(--color-brand);
        }}

        /* Containers com borda (usados para listas) */
        div[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {{
            background-color: var(--color-card);
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            border: 1px solid var(--color-border);
            padding: 1rem;
        }}
        
        /* Expanders */
        [data-testid="stExpander"] {{
            background-color: var(--color-card);
            border-radius: var(--radius) !important;
            border: 1px solid var(--color-border) !important;
            overflow: hidden;
        }}
        [data-testid="stExpander"] summary {{
            font-size: 1.05rem;
            font-weight: 500;
            color: var(--color-text);
        }}

        /* --- ELEMENTOS VISUAIS --- */

        /* Fundo da aplicação principal */
        [data-testid="stAppViewContainer"] {{
            background-color: var(--color-bg);
        }}

        /* Marca de água da mascote */
        [data-testid="stAppViewContainer"]::after {{
            content: "";
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 200px;
            height: 200px;
            background-image: url("data:image/png;base64,{mascote_b64}");
            background-size: contain;
            background-repeat: no-repeat;
            opacity: 0.1; /* Um pouco mais visível no fundo escuro */
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
