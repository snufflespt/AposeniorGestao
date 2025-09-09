import streamlit as st
from utils.ui import aplicar_estilos
from secoes import utentes, turmas, professores, disciplinas
from utils.sheets import get_worksheet

@st.cache_data(ttl=60)
def get_dashboard_stats():
    """Obtém as estatísticas para o dashboard inicial a partir das folhas de cálculo."""
    try:
        sheet_utentes = get_worksheet("Utentes")
        num_utentes = len(sheet_utentes.get_all_records())
    except Exception:
        num_utentes = "N/D"

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
        
    return num_utentes, num_disciplinas, num_turmas

# 🔹 Carregar CSS global logo no arranque
aplicar_estilos()

# Configuração global da página
st.set_page_config(page_title="Gestão IPSS", page_icon="🧭", layout="wide")


# 🔹 Logótipo no menu lateral
st.sidebar.image("imagens/logo.png", use_container_width=True)
st.sidebar.markdown("### Gestão IPSS")

st.sidebar.markdown("---")

# Menu principal
opcao = st.sidebar.radio(
    "Escolhe a secção:",
    ["🏠 Início", "📚 Disciplinas", "🧍 Utentes", "🏫 Turmas", "👨‍🏫 Professores"]
)

# Conteúdo das páginas
if opcao == "🏠 Início":
    st.title("Bem-vindo à Gestão IPSS")
    st.write("Usa o menu à esquerda para navegar entre as secções.")

    st.markdown("---")
    
    num_utentes, num_disciplinas, num_turmas = get_dashboard_stats()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="🧍 Utentes Registados", value=num_utentes)
    with col2:
        st.metric(label="📚 Disciplinas", value=num_disciplinas)
    with col3:
        st.metric(label="🏫 Turmas", value=num_turmas)
elif opcao == "📚 Disciplinas":
    disciplinas.mostrar_pagina()
elif opcao == "🧍 Utentes":
    utentes.mostrar_pagina()
elif opcao == "🏫 Turmas":
    turmas.mostrar_pagina()
elif opcao == "👨‍🏫 Professores":
    professores.mostrar_pagina()

aplicar_estilos()
