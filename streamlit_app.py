import streamlit as st
from utils.ui import aplicar_estilos
from secoes import utentes, turmas, professores, disciplinas

# 🔹 Carregar CSS global logo no arranque
aplicar_estilos()

# Configuração global da página
st.set_page_config(page_title="Gestão IPSS", page_icon="🧭", layout="wide")

# 🔹 Logótipo no menu lateral
st.sidebar.image("imagens/logo.png", use_container_width=True)
st.sidebar.markdown("### Gestão IPSS")

# Menu principal
opcao = st.sidebar.radio(
    "Escolhe a secção:",
    ["🏠 Início", "📚 Disciplinas", "🧍 Utentes", "🏫 Turmas", "👨‍🏫 Professores"]
)

# Conteúdo das páginas
if opcao == "🏠 Início":
    st.title("Bem-vindo à Gestão IPSS")
    st.write("Usa o menu à esquerda para navegar entre as secções.")
elif opcao == "📚 Disciplinas":
    disciplinas.mostrar_pagina()
elif opcao == "🧍 Utentes":
    utentes.mostrar_pagina()
elif opcao == "🏫 Turmas":
    turmas.mostrar_pagina()
elif opcao == "👨‍🏫 Professores":
    professores.mostrar_pagina()

aplicar_estilos()
