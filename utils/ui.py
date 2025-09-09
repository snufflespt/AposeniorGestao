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
            --color-bg: #f0f2f6; /* Fundo geral mais claro e moderno */
            --color-sidebar-bg: #ffffff;
            --color-text: #333333;
            --color-card: #ffffff;
            --color-brand: #F26A21;
            --color-brand-hover: #E94E1B;
            --color-border: #e0e0e0;
            --font-family: 'Inter', 'Segoe UI', sans-serif;
            --radius: 10px; /* Bordas ligeiramente mais arredondadas */
            --fs-body: 15px;
            --shadow: 0 4px 12px rgba(0, 0, 0, 0.08); /* Sombra mais suave */
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
            transform: translateY(-2px); /* Efeito de elevação subtil */
        }}

        /* Inputs e TextAreas */
        [data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea {{
            border: 1px solid var(--color-border);
            border-radius: var(--radius);
            background-color: #fafafa;
        }}
        [data-testid="stTextInput"] input:disabled, [data-testid="stTextArea"] textarea:disabled {{
            -webkit-text-fill-color: var(--color-text);
            color: var(--color-text);
            background-color: #f0f0f0;
            opacity: 0.8;
        }}

        /* Menu Lateral */
        [data-testid="stSidebar"] {{
            background-color: var(--color-sidebar-bg);
            border-right: 1px solid var(--color-border);
        }}
        
        /* Estilos para o streamlit-option-menu */
        [data-testid="stSidebar"] .nav-link {{
            font-size: 1rem; /* Tamanho da letra reduzido */
            color: #4f4f4f !important;
            border-radius: var(--radius);
            margin: 4px 0;
            transition: background-color 0.2s ease, color 0.2s ease;
        }}
        [data-testid="stSidebar"] .nav-link:hover {{
            background-color: rgba(242, 106, 33, 0.1);
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
            background-color: #fafafa;
            border-radius: var(--radius) !important;
            border: 1px solid var(--color-border) !important;
            overflow: hidden; /* Garante que os cantos arredondados sejam aplicados */
        }}
        [data-testid="stExpander"] summary {{
            font-size: 1.05rem;
            font-weight: 500;
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
            width: 200px; /* Ligeiramente menor */
            height: 200px;
            background-image: url("data:image/png;base64,{mascote_b64}");
            background-size: contain;
            background-repeat: no-repeat;
            opacity: 0.08; /* Mais subtil */
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
