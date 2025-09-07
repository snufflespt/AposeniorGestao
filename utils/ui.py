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
            --color-bg: #f7f7f7;
            --color-text: #2E2E2E;
            --color-card: #FFFFFF;
            --color-brand: #F26A21;
            --color-brand-hover: #E94E1B;

            --font-family: 'Inter', 'Segoe UI', sans-serif;

            --radius: 8px;
            --shadow: 0 2px 6px rgba(0,0,0,0.05);

            --fs-h1: 24px;
            --fs-h2: 20px;
            --fs-h3: 16px;
            --fs-body: 15px;

            --space-1: 0.25rem;  /* 4px */
            --space-2: 0.5rem;   /* 8px */
            --space-3: 0.75rem;  /* 12px */
            --space-4: 1rem;     /* 16px */
        }}

        /* Remover barra/faixa vazia no topo (Streamlit 1.49.1) */
        .block-container {{
            padding-top: 0 !important;
        }}
        .block-container > div:first-child {{
            margin-top: 0 !important;
            padding-top: 0 !important;
        }}
        .block-container h1:first-of-type {{
            margin-top: 0 !important;
        }}

        /* Fundo e tipografia global */
        html, body, [class*="css"] {{
            font-family: var(--font-family);
            background-color: var(--color-bg);
            color: var(--color-text);
            font-size: var(--fs-body);
        }}

        /* Hierarquia de títulos */
        h1 {{ font-size: var(--fs-h1); margin: var(--space-3) 0; }}
        h2 {{ font-size: var(--fs-h2); margin: var(--space-3) 0; }}
        h3 {{ font-size: var(--fs-h3); margin: var(--space-2) 0; }}

        /* Cartão de item */
        .card {{
            background: var(--color-card);
            border-radius: var(--radius);
            padding: var(--space-4) calc(var(--space-4) + 0.5rem);
            margin-bottom: var(--space-3);
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: var(--shadow);
        }}
        .card-info {{
            font-size: var(--fs-body);
            font-weight: 500;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        /* Botões dentro dos cartões */
        .card-actions button {{
            background-color: var(--color-brand);
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.4rem 0.8rem;
            font-size: 0.9rem;
            cursor: pointer;
            margin-left: var(--space-2);
            transition: background 0.2s ease;
        }}
        .card-actions button:hover {{
            background-color: var(--color-brand-hover);
        }}

        /* Alinhar verticalmente colunas */
        div[data-testid="column"] > div {{
            display: flex;
            align-items: center;
        }}

        /* Botões com altura e estilo consistentes */
        div.stButton > button {{
            background-color: #F26A21;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.4rem 0.8rem;
            font-size: 0.9rem;
            cursor: pointer;
            transition: background 0.2s ease;
        }}
        div.stButton > button:hover {{
            background-color: #E94E1B;
        }}

        /* MENU LATERAL */
        section[data-testid="stSidebar"] {{
            background-color: white;
            font-size: 1.05rem;
        }}
        section[data-testid="stSidebar"] * {{
            color: var(--color-text) !important;
        }}
        section[data-testid="stSidebar"] img {{
            display: block;
            margin: 0 auto;
            background-color: #3a3a3a;
            padding: 8px;
            border-radius: var(--radius);
            box-shadow: 0 2px 6px rgba(0,0,0,0.2);
        }}
        section[data-testid="stSidebar"] [data-testid="stImage"] {{
            background: none !important;
            padding: 0 !important;
        }}
        section[data-testid="stSidebar"] [role="radio"][aria-checked="true"] > div {{
            background-color: var(--color-brand) !important;
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
            color: var(--color-brand);
            transition: all 0.2s ease-in-out;
        }}
        button[role="tab"][aria-selected="true"] {{
            font-weight: bold !important;
            font-size: 1.10rem !important;
            border-bottom: 6px solid var(--color-brand) !important;
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

        /* Botões de ação dentro de um expander (ex: página de utentes) */
        div[data-testid="stExpander"] div[data-testid="column"]:nth-of-type(2) .stButton button {{
            width: 100%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 5px;
            box-sizing: border-box; /* Garante que o padding está incluído na largura total */
        }}

        /* Remove a margem do último botão para um alinhamento perfeito */
        div[data-testid="stExpander"] div[data-testid="column"]:nth-of-type(2) .stButton:last-child button {{
            margin-bottom: 0;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def titulo_secao(texto, icone="📌"):
    """Mostra um título de secção com divisor."""
    st.markdown(f"### {icone} {texto}")
    st.divider()
