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
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
        
        <style>
        :root {{
            --color-text: #4E443A; /* Castanho escuro para texto, bom contraste em fundos claros */
            --color-card: rgba(255, 255, 255, 0.7); /* Efeito de vidro fosco */
            --color-sidebar-bg: rgba(255, 255, 255, 0.6);
            --color-brand-start: #D90429; /* Vermelho-fogo */
            --color-brand-end: #FF930F; /* Laranja-dourado */
            --color-border: rgba(255, 255, 255, 0.9); /* Borda muito subtil */
            --font-family: 'Montserrat', sans-serif;
            --radius: 12px; /* Um pouco mais arredondado */
            --fs-body: 15px;
            --shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
        }}

        /* --- CONFIGURAÇÕES GLOBAIS --- */
        
        html, body, [class*="css"] {{
            font-family: var(--font-family);
            color: var(--color-text);
            font-size: var(--fs-body);
        }}
        
        .block-container {{
            padding-top: 2rem !important;
        }}

        /* --- ESTILOS DE COMPONENTES --- */

        /* Botão Geral com Gradiente */
        [data-testid="stButton"] > button {{
            background: linear-gradient(90deg, var(--color-brand-start), var(--color-brand-end));
            color: white;
            border: none;
            border-radius: var(--radius);
            padding: 0.6rem 1.2rem;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            box-shadow: 0 4px 10px rgba(240, 90, 20, 0.3);
        }}
        [data-testid="stButton"] > button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 6px 15px rgba(240, 90, 20, 0.4);
        }}

        /* Inputs e TextAreas */
        [data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea, [data-testid="stSelectbox"] div[data-baseweb="select"] > div {{
            border: 1px solid var(--color-border);
            border-radius: var(--radius);
            background-color: rgba(255, 255, 255, 0.8);
            color: var(--color-text);
        }}
        [data-testid="stTextInput"] input:disabled, [data-testid="stTextArea"] textarea:disabled {{
            -webkit-text-fill-color: #888;
            color: #888;
            background-color: rgba(255, 255, 255, 0.5);
        }}

        /* Menu Lateral */
        [data-testid="stSidebar"] {{
            background-color: var(--color-sidebar-bg);
            border-right: 1px solid var(--color-border);
            backdrop-filter: blur(10px); /* Efeito de vidro */
        }}
        
        /* Estilos para o streamlit-option-menu */
        [data-testid="stSidebar"] .nav-link {{
            font-size: 1rem;
            color: var(--color-text) !important;
            border-radius: var(--radius);
            margin: 4px 0;
            transition: all 0.2s ease;
        }}
        [data-testid="stSidebar"] .nav-link:hover {{
            background-color: rgba(255, 255, 255, 0.3);
        }}
        [data-testid="stSidebar"] .nav-link-selected {{
            background: linear-gradient(90deg, var(--color-brand-start), var(--color-brand-end));
            color: white !important;
            font-weight: 600;
        }}

        /* Abas (Tabs) */
        button[role="tab"] {{
            color: var(--color-text);
        }}
        button[role="tab"][aria-selected="true"] {{
            font-weight: 600;
            background-color: var(--color-card);
            border-image: linear-gradient(90deg, var(--color-brand-start), var(--color-brand-end)) 1;
            border-bottom-width: 3px;
            border-bottom-style: solid;
        }}

        /* Métricas no Dashboard */
        [data-testid="stMetric"] {{
            background-color: var(--color-card);
            backdrop-filter: blur(10px);
            border-radius: var(--radius);
            padding: 1.5rem;
            box-shadow: var(--shadow);
            border-left: 5px solid;
            border-image: linear-gradient(to bottom, var(--color-brand-start), var(--color-brand-end)) 1;
        }}

        /* Containers e Expanders */
        div[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"], [data-testid="stExpander"] {{
            background-color: var(--color-card);
            backdrop-filter: blur(10px);
            border-radius: var(--radius) !important;
            box-shadow: var(--shadow);
            border: 1px solid var(--color-border);
            padding: 1rem;
            overflow: hidden;
        }}
        [data-testid="stExpander"] summary {{
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--color-text);
        }}

        /* --- ELEMENTOS VISUAIS --- */

        /* Fundo da aplicação principal com gradiente */
        [data-testid="stAppViewContainer"] {{
            background: linear-gradient(135deg, #FFDDC1 0%, #FFECB3 100%);
            background-attachment: fixed;
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
            opacity: 0.25; /* Mais visível no fundo claro */
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
