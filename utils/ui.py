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
            --fs-body: 15px;
        }}

        /* --- CONFIGURAÇÕES GLOBAIS --- */
        
        /* Fundo e tipografia */
        html, body, [class*="css"] {{
            font-family: var(--font-family);
            background-color: var(--color-bg);
            color: var(--color-text);
            font-size: var(--fs-body);
        }}
        
        /* Adiciona espaçamento no topo da página */
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
            padding: 0.5rem 1rem;
            font-size: 0.95rem;
            cursor: pointer;
            transition: background-color 0.2s ease;
        }}
        [data-testid="stButton"] > button:hover {{
            background-color: var(--color-brand-hover);
        }}

        /* Inputs de Texto (geral e desativado) */
        [data-testid="stTextInput"] input {{
            border: 1px solid #ccc;
            border-radius: var(--radius);
        }}
        /* Garante que o texto em campos desativados seja legível */
        [data-testid="stTextInput"] input:disabled {{
            -webkit-text-fill-color: var(--color-text); /* Para Chrome/Safari */
            color: var(--color-text); /* Para outros browsers */
            background-color: #fafafa; /* Fundo cinza claro para indicar que está desativado */
        }}

        /* Menu Lateral */
        [data-testid="stSidebar"] {{
            background-color: #3a3a3a; /* Cinza escuro para contraste com o logo */
        }}
        [data-testid="stSidebar"] [role="radio"][aria-checked="true"] > div {{
            background-color: var(--color-brand) !important;
            border-radius: var(--radius);
            font-weight: bold !important;
            color: white !important;
        }}
        
        /* Abas (Tabs) */
        button[role="tab"] {{
            font-size: 1.05rem;
        }}
        button[role="tab"][aria-selected="true"] {{
            font-weight: bold;
            border-bottom: 3px solid var(--color-brand);
        }}

        /* --- ESTILOS ESPECÍFICOS DE PÁGINAS --- */

        /* Botões na página de Utentes (Editar/Apagar) para terem o mesmo tamanho */
        div[data-testid="stExpander"] div[data-testid="column"] [data-testid="stButton"] > button {{
            width: 100%; /* Força o botão a ocupar toda a largura da sua coluna */
            margin-bottom: 0.5rem; /* Adiciona espaço vertical entre os botões */
        }}
        /* Remove a margem do último botão para um alinhamento perfeito */
        div[data-testid="stExpander"] div[data-testid="column"] > div:last-of-type [data-testid="stButton"] > button {{
            margin-bottom: 0; 
        }}

        /* --- ELEMENTOS VISUAIS --- */

        /* Fundo da aplicação principal */
        [data-testid="stAppViewContainer"] {{
            background: linear-gradient(135deg, #e8e1da 0%, #d8ccc2 100%);
            background-attachment: fixed;
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
            opacity: 0.15; /* Ligeiramente mais subtil para não distrair */
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
