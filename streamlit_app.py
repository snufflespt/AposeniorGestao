import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from utils.ui import aplicar_estilos
from secoes import utentes, turmas, professores, disciplinas, horarios
from utils.sheets import get_worksheet

@st.cache_data(ttl=60)
def get_dashboard_stats():
    """Obtém as estatísticas para o dashboard inicial a partir das folhas de cálculo."""
    try:
        sheet_utentes = get_worksheet("Utentes")
        dados_utentes = sheet_utentes.get_all_records()
        if dados_utentes:
            df_utentes = pd.DataFrame(dados_utentes)
            num_utentes = len(df_utentes)
            if 'Estado' in df_utentes.columns:
                num_utentes_ativos = df_utentes[df_utentes['Estado'] == 'Ativo'].shape[0]
                num_utentes_inativos = df_utentes[df_utentes['Estado'] == 'Inativo'].shape[0]
            else:
                num_utentes_ativos = "N/A"
                num_utentes_inativos = "N/A"
        else:
            num_utentes = 0
            num_utentes_ativos = 0
            num_utentes_inativos = 0
    except Exception:
        num_utentes = "N/D"
        num_utentes_ativos = "N/D"
        num_utentes_inativos = "N/D"

    try:
        sheet_disciplinas = get_worksheet("Disciplinas")
        num_disciplinas = len(sheet_disciplinas.get_all_records())
    except Exception:
        num_disciplinas = "N/D"
    
    try:
        sheet_turmas = get_worksheet("Turmas")
        num_turmas = len(sheet_turmas.get_all_records())
    except Exception:
        num_turmas = "N/D"
        
    return num_utentes, num_utentes_ativos, num_utentes_inativos, num_disciplinas, num_turmas

# Configuração global da página
st.set_page_config(page_title="Gestão IPSS", page_icon="🧭", layout="wide")

# 🔹 Carregar CSS global logo no arranque
aplicar_estilos()


# 🔹 Logótipo no menu lateral
st.sidebar.image("imagens/logo.png")
st.sidebar.markdown("### Gestão IPSS")

st.sidebar.markdown("---")

# Menu principal
with st.sidebar:
    opcao = option_menu(
        menu_title="Menu",
        options=["Início", "Disciplinas", "Utentes", "Turmas", "Horários", "Professores"],
        icons=["house-door", "book", "people", "building-gear", "calendar3", "person-badge"],
        menu_icon="grid-1x2",
        default_index=0,
        orientation="vertical",
    )

# Conteúdo das páginas
if opcao == "Início":
    st.title("Bem-vindo à Gestão IPSS")
    st.write("Usa o menu à esquerda para navegar entre as secções.")

    st.markdown("---")
    
    num_utentes, num_utentes_ativos, num_utentes_inativos, num_disciplinas, num_turmas = get_dashboard_stats()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric(label="🧍 Utentes (Total)", value=num_utentes)
    with col2:
        st.metric(label="✅ Utentes Ativos", value=num_utentes_ativos)
    with col3:
        st.metric(label="❌ Utentes Inativos", value=num_utentes_inativos)
    with col4:
        st.metric(label="📚 Disciplinas", value=num_disciplinas)
    with col5:
        st.metric(label="🏫 Turmas", value=num_turmas)
elif opcao == "Disciplinas":
    disciplinas.mostrar_pagina()
elif opcao == "Utentes":
    utentes.mostrar_pagina()
elif opcao == "Turmas":
    turmas.mostrar_pagina()
elif opcao == "Horários":
    horarios.mostrar_pagina()
elif opcao == "Professores":
    professores.mostrar_pagina()
