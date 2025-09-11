import streamlit as st
st.cache_data.clear()
import pandas as pd
from streamlit_option_menu import option_menu
from utils.ui import aplicar_estilos
from secoes import utentes, turmas, professores, disciplinas, horarios
from utils.sheets import get_worksheet

@st.cache_data(ttl=300)
def get_dashboard_stats():
    """Retorna estatísticas simuladas para o dashboard inicial"""
    # Dados simulados para demonstração
    num_utentes = 150
    num_utentes_ativos = 120
    num_utentes_inativos = 30
    num_disciplinas = 25
    num_turmas = 18
    return num_utentes, num_utentes_ativos, num_utentes_inativos, num_disciplinas, num_turmas

# Configuração global da página
st.set_page_config(page_title="Gestão IPSS", page_icon="🧭", layout="wide")

# 🔹 Carregar CSS global logo no arranque
print("aplicar_estilos() called")
aplicar_estilos()

# 🔹 Aplicar fundo azul e estilos dos cartões de professores
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle, #34495e 0%, #2c3e50 100%) !important;
}
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle, #34495e 0%, #2c3e50 100%) !important;
}
html, body, [class*="css"] {
    background: radial-gradient(circle, #34495e 0%, #2c3e50 100%) !important;
}

/* Estilos gerais mantidos apenas para fundo da aplicação */
</style>
""", unsafe_allow_html=True)


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
