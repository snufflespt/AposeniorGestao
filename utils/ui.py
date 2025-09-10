import streamlit as st
import base64


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
            --color-bg-start: #34495e; /* Azul médio para melhor legibilidade */
            --color-bg-end: #2c3e50; /* Tom mais claro do gradiente */
            --color-sidebar-bg: #1f2c39;
            --color-text: #FFFFFF; /* Branco 100% puro para máxima legibilidade */
            --color-card: #6c7b8d; /* Cinza-azulado médio para melhor contraste */
            --color-card-contrast: #ecf0f1; /* Branco-nuvem para máximo contraste */
            --color-brand-start: #e74c3c; /* Vermelho mais vibrante */
            --color-brand-end: #f39c12; /* Laranja mais brilhante */
            --color-border: #95a5a6; /* Borda muito clara e visível */
            --color-border-strong: #bdc3c7; /* Borda ainda mais clara para divisórias */
            --color-divider: #7f8c8d; /* Cinza médio forte para divisórias */
            --color-success: #27ae60; /* Verde sucesso */
            --color-warning: #f1c40f; /* Amarelo aviso */
            --color-error: #e74c3c; /* Vermelho erro */
            --font-family: 'Montserrat', sans-serif;
            --radius: 12px;
            --fs-body: 15px;
            --shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
            --divider-height: 3px; /* Divisórias mais grossas */
        }}

        /* --- CONFIGURAÇÕES GLOBAIS --- */

        html, body, [class*="css"] {{
            font-family: var(--font-family);
            color: var(--color-text) !important;
            font-size: var(--fs-body);
            background: radial-gradient(circle, #34495e 0%, #2c3e50 100%) !important;
        }}

        /* DESTAQUE AZUL CLARO PARA FORMULÁRIOS E CARDS */
        [data-testid="stForm"], .form-container {{
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%) !important;
            border-radius: var(--radius) !important;
            padding: 20px !important;
            margin: 20px 0 !important;
            border: 1px solid #546e7a !important;
            box-shadow: 0 8px 32px rgba(52, 73, 94, 0.4) !important;
        }}
        .card-container {{
            background: linear-gradient(135deg, #74b9ff 0%, #3498db 100%) !important;
            border-radius: var(--radius) !important;
            padding: 15px !important;
            margin: 10px 0 !important;
            border: 1px solid #546e7a !important;
            box-shadow: 0 6px 24px rgba(52, 73, 94, 0.3) !important;
        }}

        /* Containers de abas com destaque azul */
        [data-testid*="stTabs"] > div > div {{
            background: linear-gradient(135deg, #74b9ff 0%, #3498db 100%) !important;
            border-radius: 12px 12px 0 0 !important;
            margin-bottom: 0 !important;
        }}

        /* Área de formulário mais escura para contraste */
        .element-container:has([data-testid="stForm"]) {{
            background: rgba(65, 90, 119, 0.6) !important;
            border-radius: var(--radius) !important;
            padding: 15px !important;
            margin: 10px 0 !important;
        }}

        .block-container {{
            padding-top: 2rem !important;
        }}

        /* TÍTULOS BRANCOS - Correção específica */
        [data-testid="stMarkdownContainer"] h1,
        [data-testid="stMarkdownContainer"] h2,
        [data-testid="stMarkdownContainer"] h3,
        [data-testid="stMarkdownContainer"] h4,
        [data-testid="stMarkdownContainer"] h5,
        [data-testid="stMarkdownContainer"] h6 {{
            color: white !important;
            font-weight: 600 !important;
        }}

        /* Títulos específicos das páginas */
        [data-testid="stText"] h1,
        [data-testid="stText"] h2,
        [data-testid="stText"] h3 {{
            color: white !important;
        }}

        /* TÍTULOS BRANCOS - Todos os títulos e subtítulos */
        h1, h2, h3, h4, h5, h6 {{
            color: white !important;
            font-weight: 600 !important;
        }}

        /* Títulos em markdown containers */
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
        .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {{
            color: white !important;
            font-weight: 600 !important;
        }}

        /* Títulos específicos das seções */
        [data-testid*="stMarkdownContainer"] h1,
        [data-testid*="stMarkdownContainer"] h2,
        [data-testid*="stMarkdownContainer"] h3,
        [data-testid*="stMarkdownContainer"] h4,
        [data-testid*="stMarkdownContainer"] h5,
        [data-testid*="stMarkdownContainer"] h6 {{
            color: white !important;
            font-weight: 600 !important;
        }}

        /* TEXTO GERAL BRANCO - Texto comum que ainda não está coberto */
        p, span, div, label {{
            color: white !important;
        }}

        /* Texto específica em tabelas e listas */
        [data-testid="stDataFrame"], [data-testid="stTable"] {{
            color: #2c3e50 !important;
        }}

        /* Override específico para tabelas - fundo branco, texto preto */
        [data-testid="stDataFrame"] tbody tr, [data-testid="stTable"] tbody tr {{
            background-color: white !important;
            color: #2c3e50 !important;
        }}

        /* Texto de paginação e status - como "Mostrando X de X" */
        .stSelectbox, .stMultiSelect, [data-testid*="stText"] {{
            color: white !important;
        }}

        /* Texto em containers especiais */
        .element-container p, .element-container span, .element-container div {{
            color: white !important;
        }}

        /* Exceção para conteúdo dentro de formulários que já foi tratado */
        .element-container div:has([data-testid*="stTextInput"]),
        .element-container div:has([data-testid*="stNumberInput"]) {{
            color: var(--color-text) !important;
        }}

        /* --- ESTILOS DE COMPONENTES --- */

        /* Alertas (st.warning, st.info, etc.) */
        [data-testid="stAlert"] {{
            background-color: var(--color-card-contrast) !important;
            color: #2c3e50 !important; /* Cor de texto escura para contraste */
            border-radius: var(--radius);
            border-left: 4px solid;
        }}
        [data-testid="stAlert"] p {{
            color: #2c3e50 !important; /* Texto escuro para melhor leitura */
            font-weight: 500;
        }}

        /* Messages de sucesso, erro e informações */
        div[role="alert"], .css-1gr6cnr {{
            background-color: rgba(255, 255, 255, 0.95) !important;
            border: 1px solid var(--color-border) !important;
            border-radius: var(--radius);
            color: #2c3e50 !important;
        }}

        /* Textos importantes com fundo xácido */
        .element-container div:has([data-testid*="TextArea"]), .element-container div:has([data-testid*="TextInput"]) {{
            background-color: rgba(255, 255, 255, 0.05) !important;
            border-radius: var(--radius);
            padding: 0.5rem;
        }}

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
            background-color: var(--color-bg-start);
            color: var(--color-text) !important;
        }}
        [data-testid="stTextInput"] input:disabled, [data-testid="stTextArea"] textarea:disabled {{
            -webkit-text-fill-color: #bdc3c7; /* Cinza mais claro */
            color: #bdc3c7; /* Cinza mais claro */
            background-color: #2c3e50;
            opacity: 0.7;
        }}

        /* FORMULÁRIOS COMPLETOS - Labels brancos + fundo branco */
        [data-testid="stTextInput"] label,
        [data-testid="stNumberInput"] label,
        [data-testid="stTextArea"] label,
        [data-testid="stSelectbox"] label,
        [data-testid="stDateInput"] label,
        [data-testid="stTimeInput"] label {{
            color: white !important;
            font-weight: 600 !important;
            font-size: 14px !important;
        }}

        /* Todos os campos de entrada com fundo branco */
        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea,
        [data-testid="stNumberInput"] input,
        [data-testid="stNumberInput"] input[type="number"],
        [data-testid="stSelectbox"] input,
        [data-testid="stSelectbox"] div[data-baseweb="select"] input {{
            background-color: white !important;
            color: #2c3e50 !important;
            border: 1px solid #ddd !important;
            border-radius: var(--radius) !important;
            font-weight: 500 !important;
        }}

        /* Campos de data e tempo */
        [data-testid="stDateInput"] input,
        [data-testid="stTimeInput"] input {{
            background-color: white !important;
            color: #2c3e50 !important;
            border: 1px solid #ddd !important;
        }}

        /* Campos de seleção (dropdowns) */
        [data-testid="stSelectbox"] div[data-baseweb="select"] {{
            background-color: white !important;
            border: 1px solid #ddd !important;
            border-radius: var(--radius) !important;
        }}

        [data-testid="stSelectbox"] div[data-baseweb="select"] div {{
            color: #2c3e50 !important;
        }}

        /* GARANTIR BOTÕES COM GRADIENTE - Todos os botões */
        button[data-testid*="baseButton"], .stButton > button {{
            background: linear-gradient(90deg, var(--color-brand-start), var(--color-brand-end)) !important;
            color: white !important;
            border: none !important;
            border-radius: var(--radius) !important;
            padding: 0.6rem 1.2rem !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 10px rgba(240, 90, 20, 0.3) !important;
        }}

        /* Botão "Guardar professor" específico */
        button[kind="primary"], button:contains("Guardar"), button:contains("Submit") {{
            background: linear-gradient(90deg, var(--color-brand-start), var(--color-brand-end)) !important;
        }}

        /* MENU LATERAL MELHORADO */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, var(--color-bg-start), var(--color-bg-end)) !important;
            border-right: 2px solid var(--color-border);
            box-shadow: 6px 0 20px rgba(0, 0, 0, 0.25), 0 0 60px rgba(231, 76, 60, 0.1) !important;
            border-radius: 0 10px 10px 0 !important;
        }}

        /* MENU LATERAL - STREAMLIT OPTION MENU */
        [data-testid="stSidebar"] .css-1quwbsr {{"""
    """}}

        /* Seleção com gradiente consistente Streamlit Option Menu */
        [data-testid="stSidebar"] ul li div[data-testid="stVerticalBlock"] div.record-header {{"""
    """}}
        [data-testid="stSidebar"] .nav-link, [data-testid="stSidebar"] a {{"""
    """}}

        /* Streamlit Option Menu - pilares principais */
        [data-testid="stSidebar"] ._option-menu-container .option-menu-container .option-menu-item {{"""
    """}}

        /* Estilização correta do Streamlit Option Menu */
        [data-testid="stSidebar"] button[data-v-b9058cd2] {{"""
    """}}

        /* MENU ESTILIZADO PARA STREAMLIT-OPTION-MENU */
        [data-testid="stSidebar"] .nav-link {{
            font-size: 1.1rem !important;
            color: var(--color-text) !important;
            border-radius: var(--radius) !important;
            margin: 6px 8px !important;
            padding: 14px 18px !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            border-left: 4px solid transparent !important;
            font-weight: 500 !important;
            text-decoration: none !important;
            background: rgba(255, 255, 255, 0.02) !important;
            backdrop-filter: blur(8px) !important;
            position: relative !important;
            overflow: hidden !important;
        }}

        /* Efeito de brilho no hover */
        [data-testid="stSidebar"] .nav-link::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.5s;
        }}

        /* Hover effect simples e elegante */
        [data-testid="stSidebar"] .nav-link:hover {{
            background: rgba(255, 255, 255, 0.08) !important;
            transform: translateX(4px) !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
            color: white !important;
        }}

        [data-testid="stSidebar"] .nav-link:hover::before {{
            left: 100%;
        }}

        /* Seleção com gradiente consistente e micro-animação */
        [data-testid="stSidebar"] .nav-link-selected {{
            background: linear-gradient(135deg, var(--color-brand-start) 0%, var(--color-brand-end) 100%) !important;
            color: white !important;
            font-weight: 600 !important;
            border-left-color: white !important;
            box-shadow: 0 6px 25px rgba(231, 76, 60, 0.4), 0 0 50px rgba(243, 156, 18, 0.2) !important;
            transform: translateX(8px) scale(1.02) !important;
            border-radius: 12px !important;
            position: relative !important;
            animation: pulse-selected 2s infinite !important;
        }}

        /* Animação sutil para item selecionado */
        @keyframes pulse-selected {{
            0%, 100% {{
                box-shadow: 0 6px 25px rgba(231, 76, 60, 0.4), 0 0 30px rgba(243, 156, 18, 0.1);
            }}
            50% {{
                box-shadow: 0 6px 25px rgba(231, 76, 60, 0.6), 0 0 40px rgba(243, 156, 18, 0.2);
            }}
        }}

        /* Ícones dos menus com melhor espaçamento */
        [data-testid="stSidebar"] .nav-link i,
        [data-testid="stSidebar"] .nav-link svg {{"""
    """}}

        /* Título do sidebar */
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {{
            color: white !important;
            font-weight: 700 !important;
            text-align: center !important;
            margin-bottom: 20px !important;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2) !important;
        }}

        /* Abas (Tabs) */
        button[role="tab"] {{
            color: var(--color-text) !important;
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
            border-radius: var(--radius);
            padding: 1.5rem;
            box-shadow: var(--shadow);
            border-left: 5px solid;
            border-image: linear-gradient(to bottom, var(--color-brand-start), var(--color-brand-end)) 1;
        }}

        /* CARTÕES DE PROFESSORES - AZUL CLARO FUNCIONAL */
        /* Aplicar fundo azul-claro diretamente no HTML dos summaries */
        details summary {{
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%) !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 16px 20px !important;
            border-radius: var(--radius) var(--radius) 0 0 !important;
            cursor: pointer !important;
            transition: all 0.2s ease !important;
        }}

        /* Garantir que streamlit summary também pegue */
        [data-testid="stExpander"] summary {{
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%) !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 16px 20px !important;
            border-radius: var(--radius) var(--radius) 0 0 !important;
            cursor: pointer !important;
            transition: all 0.2s ease !important;
        }}

        /* Efeito hover azul ainda mais claro */
        details summary:hover, [data-testid="stExpander"] summary:hover {{
            background: linear-gradient(135deg, #5dade2 0%, #3498db 100%) !important;
            transform: translateY(-1px) !important;
        }}

        /* Conteúdo expandido com fundo azul */
        [data-testid="stExpander"][aria-expanded="true"] [data-testid*="stVerticalBlock"] {{
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%) !important;
            padding: 20px !important;
            border-radius: 0 0 var(--radius) var(--radius) !important;
            border-top: 1px solid #546e7a !important;
        }}

        /* Divisórias mais visíveis */
        hr {{
            border: none;
            height: var(--divider-height);
            background: var(--color-divider);
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            margin: 1.5rem 0;
        }}

        /* Linhas divisoras em elementos Streamlit */
        [data-testid="stVerticalBlockBorderWrapper"]::before {{
            content: "";
            display: block;
            height: 2px;
            background: linear-gradient(90deg, var(--color-border-strong), var(--color-divider), var(--color-border-strong));
            margin: 1rem 0;
            border-radius: 1px;
        }}

        /* Separadores entre cards */
        .element-container {{
            border-bottom: 1px solid var(--color-border) !important;
        }}

        /* --- ELEMENTOS VISUAIS --- */

        /* Fundo da aplicação principal com gradiente */
        [data-testid="stAppViewContainer"] {{
            background: radial-gradient(circle, #34495e 0%, #2c3e50 100%);
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
            opacity: 0.2; /* Mais visível */
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
