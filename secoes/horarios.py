import streamlit as st
import pandas as pd
from utils.sheets import get_worksheet
from utils.ui import configurar_pagina, titulo_secao

# Ordem dos dias da semana para a visualização
DIAS_SEMANA_ORDEM = [
    "Segunda-feira", "Terça-feira", "Quarta-feira", 
    "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"
]

@st.cache_data(ttl=60)
def carregar_dados_turmas():
    """
    Carrega e processa os dados das turmas da folha de cálculo.

    Returns:
        pd.DataFrame: DataFrame com os dados das turmas ativas, 
                      ou um DataFrame vazio em caso de erro.
    """
    try:
        sheet_turmas = get_worksheet("Turmas")
        dados = sheet_turmas.get_all_records()
        if not dados:
            return pd.DataFrame()
        
        df = pd.DataFrame(dados)
        
        # Filtrar apenas turmas ativas, se a coluna 'Estado' existir
        if 'Estado' in df.columns:
            df = df[df['Estado'] == 'Ativa']
            
        # Ordenar por hora de início para uma visualização cronológica
        if 'Hora de Inicio' in df.columns:
            df = df.sort_values(by='Hora de Inicio')
            
        return df
    except Exception as e:
        st.error(f"Não foi possível carregar os horários: {e}")
        return pd.DataFrame()

def mostrar_pagina():
    """Renderiza a página de visualização de horários."""
    configurar_pagina("Horários", "🗓️")
    titulo_secao("Horário Semanal das Turmas", "🗓️")

    df_turmas = carregar_dados_turmas()

    if df_turmas.empty:
        st.info("Não existem turmas ativas para apresentar no horário.")
        return

    # Criar colunas para cada dia da semana
    cols = st.columns(len(DIAS_SEMANA_ORDEM))

    for i, dia in enumerate(DIAS_SEMANA_ORDEM):
        with cols[i]:
            st.markdown(f"##### {dia}")
            turmas_dia = df_turmas[df_turmas['Dia da Semana'] == dia]

            if turmas_dia.empty:
                st.markdown("_Sem aulas_")
            else:
                for _, turma in turmas_dia.iterrows():
                    with st.container(border=True):
                        st.markdown(f"**{turma.get('Nome da Turma', 'N/A')}**")
                        st.markdown(f"🕒 `{turma.get('Hora de Inicio', '')} - {turma.get('Hora de Fim', '')}`")
                        st.markdown(f"👨‍🏫 {turma.get('Professor', 'N/A')}")
                        
                        sala = turma.get('Sala', 'N/A')
                        if sala == "Outro":
                            sala = turma.get('Outro_Local', 'Outro')
                        st.markdown(f"🚪 {sala}")
