# disciplinas.py
import streamlit as st
import pandas as pd

def mostrar_pagina():
    st.header("📚 Disciplinas")

    # 1) Obter dados (ajusta isto à tua origem real)
    # Exemplo: tentar ler do session_state, senão criar um DF vazio com colunas esperadas
    df = st.session_state.get(
        "disciplinas_df",
        pd.DataFrame(columns=["Nome da Disciplina", "Código"])
    )

    # 2) Filtro de pesquisa
    termo = st.text_input("Procurar", placeholder="Nome ou código...")
    if termo:
        mask = (
            df["Nome da Disciplina"].astype(str).str.contains(termo, case=False, na=False)
            | df["Código"].astype(str).str.contains(termo, case=False, na=False)
        )
        df_filtrado = df[mask]
    else:
        df_filtrado = df

    st.write(f"{len(df_filtrado)} disciplinas encontradas.")

    # 3) Listagem com ações alinhadas e botões juntos
    for i, row in df_filtrado.iterrows():
        # Alinhamento vertical (fallback se versão não suportar)
        try:
            col_info, col_actions = st.columns([8, 2], vertical_alignment="center")
        except TypeError:
            col_info, col_actions = st.columns([8, 2])

        # Texto numa única linha (ellipsis)
        nome = row.get("Nome da Disciplina", "")
        cod = row.get("Código", "")
        col_info.markdown(
            f'<div class="linha-texto">{nome} — {cod}</div>',
            unsafe_allow_html=True
        )

        # Dois botões na MESMA coluna, lado a lado
        a1, a2 = col_actions.columns(2)
        with a1:
            if st.button("✏️ Editar", key=f"edit_disc_{i}", use_container_width=True):
                st.session_state["edit_disc_index"] = i
        with a2:
            if st.button("🗑️ Apagar", key=f"delete_disc_{i}", use_container_width=True):
                st.session_state["delete_disc_index"] = i
