import streamlit as st
import pandas as pd
import time
import unicodedata
from datetime import time as time_obj
from utils.sheets import get_worksheet
from utils.ui import configurar_pagina, titulo_secao

# --- Funções Auxiliares ---

def normalize_string(s):
    """Remove acentos e converte para minúsculas para comparação."""
    if not s or not isinstance(s, str): return ""
    s = unicodedata.normalize('NFD', s.lower())
    s = s.encode('ascii', 'ignore').decode('utf-8')
    return s

def check_time_overlap(start1, end1, start2, end2):
    """Verifica se dois intervalos de tempo se sobrepõem."""
    return start1 < end2 and start2 < end1

# --- Constantes ---

SALA_OPCOES = ["Sala 1", "Sala 2", "Sala 3", "Sala de Artes", "Sala Exterior", "Outro"]
DIAS_SEMANA = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
NIVEL_OPCOES = ["Inicial", "Intermédio-Inicial", "Intermédio", "Intermédio-Avançado", "Avançado", "Outro"]
ESTADO_OPCOES = ["Ativa", "Inativa"]

def mostrar_pagina():
    if 'form_turma_key' not in st.session_state:
        st.session_state.form_turma_key = 0

    sheet_turmas = get_worksheet("Turmas")
    sheet_disc = get_worksheet("Disciplinas")
    sheet_prof = get_worksheet("Professores")

    # Obter listas de opções
    try:
        disciplinas = ["-- Selecione --"] + sheet_disc.col_values(2)[1:]  # Coluna B: Nome da Disciplina
        professores = ["-- Selecione --"] + sheet_prof.col_values(2)[1:] # Coluna B: Nome Completo
    except Exception as e:
        st.error(f"Não foi possível carregar as listas de disciplinas ou professores: {e}")
        disciplinas = ["-- Selecione --"]
        professores = ["-- Selecione --"]

    tab_adicionar, tab_gerir = st.tabs(["➕ Adicionar turma", "📋 Gerir turmas"])

    with tab_adicionar:
        titulo_secao("Adicionar nova turma", "➕")
        with st.form(f"form_turma_{st.session_state.form_turma_key}"):
            col1, col2 = st.columns(2)
            with col1:
                nome_turma = st.text_input("✍️ **Nome da turma**")
                disciplina = st.selectbox("📚 **Disciplina**", options=disciplinas)
                professor = st.selectbox("👨‍🏫 **Professor**", options=professores)
                sala = st.selectbox("🚪 **Sala**", options=SALA_OPCOES)
                outro_local = st.text_input("📍 **Especifique o local**", disabled=(sala != "Outro"))
            with col2:
                dia_semana = st.selectbox("🗓️ **Dia da Semana**", options=DIAS_SEMANA)
                hora_inicio = st.time_input("⏰ **Hora de Início**")
                hora_fim = st.time_input("🏁 **Hora de Fim**")
                vagas = st.number_input("👥 **Número de vagas**", min_value=1, step=1)

            nivel = st.selectbox("📶 **Nível**", options=NIVEL_OPCOES)
            estado = st.selectbox("📊 **Estado**", options=ESTADO_OPCOES)
            observacoes = st.text_area("📝 **Observações**")
            
            b_col1, b_col2, _ = st.columns([1, 1, 5])
            with b_col1:
                submit_guardar = st.form_submit_button("Guardar", type="primary")
            with b_col2:
                submit_limpar = st.form_submit_button("Limpar")

        if submit_limpar:
            st.session_state.form_turma_key += 1
            st.rerun()

        if submit_guardar:
            # --- Validações ---
            erros = []
            if not nome_turma.strip(): erros.append("Nome da turma é obrigatório.")
            if disciplina == "-- Selecione --": erros.append("Disciplina é obrigatória.")
            if professor == "-- Selecione --": erros.append("Professor é obrigatório.")
            if sala == "Outro" and not outro_local.strip(): erros.append("Especifique o local é obrigatório quando a sala é 'Outro'.")
            if hora_fim <= hora_inicio: erros.append("A Hora de Fim deve ser posterior à Hora de Início.")

            if erros:
                st.error("Por favor, corrija os seguintes erros:\n- " + "\n- ".join(erros))
            else:
                dados_atuais = sheet_turmas.get_all_records()
                conflitos = []
                # Validar conflitos de horário
                for turma in dados_atuais:
                    if turma.get('Dia da Semana') == dia_semana:
                        try:
                            turma_inicio = time_obj.fromisoformat(turma.get('Hora de Inicio'))
                            turma_fim = time_obj.fromisoformat(turma.get('Hora de Fim'))
                            if check_time_overlap(hora_inicio, hora_fim, turma_inicio, turma_fim):
                                if sala != "Outro" and turma.get('Sala') == sala:
                                    conflitos.append(f"Sala '{sala}' já está ocupada neste horário.")
                                if turma.get('Professor') == professor:
                                    conflitos.append(f"Professor '{professor}' já tem uma aula neste horário.")
                        except (ValueError, TypeError):
                            continue # Ignora turmas com formato de hora inválido

                # Validar nome único por disciplina
                for turma in dados_atuais:
                    if normalize_string(turma.get('Nome turma')) == normalize_string(nome_turma) and turma.get('Disciplina') == disciplina:
                        conflitos.append(f"O nome '{nome_turma}' já existe para a disciplina '{disciplina}'.")
                        break

                if conflitos:
                    st.error("Foram encontrados os seguintes conflitos:\n- " + "\n- ".join(conflitos))
                else:
                    # Gerar ID
                    if not dados_atuais: proximo_id_num = 1
                    else:
                        max_id = 0
                        for r in dados_atuais:
                            try:
                                id_num = int(r.get('ID_Turma', 'T0').split('T')[-1])
                                if id_num > max_id: max_id = id_num
                            except (ValueError, TypeError): continue
                        proximo_id_num = max_id + 1
                    novo_id = f"T{proximo_id_num:04d}"
                    
                    # Guardar dados
                    nova_linha = [
                        novo_id, nome_turma, disciplina, professor, sala, 
                        outro_local if sala == "Outro" else "", dia_semana, 
                        hora_inicio.strftime('%H:%M'), hora_fim.strftime('%H:%M'), vagas,
                        nivel, estado, observacoes
                    ]
                    sheet_turmas.append_row(nova_linha)
                    st.success(f"Turma '{nome_turma}' adicionada com sucesso!")
                    st.session_state.form_turma_key += 1
                    st.rerun()

    with tab_gerir:
        dados = sheet_turmas.get_all_records()
        if not dados:
            st.info("Ainda não existem turmas registadas.")
        else:
            df = pd.DataFrame(dados)

            # --- VISTA DE EDIÇÃO ---
            if 'edit_turma_index' in st.session_state:
                idx = st.session_state['edit_turma_index']
                turma_atual = df.loc[idx]

                if st.button("⬅️ Voltar à lista"):
                    del st.session_state['edit_turma_index']
                    st.rerun()
                
                st.subheader(f"Editar turma: {turma_atual.get('Nome turma')}")
                with st.form("form_editar_turma"):
                    col1, col2 = st.columns(2)
                    with col1:
                        novo_nome = st.text_input("✍️ **Nome da turma**", value=turma_atual.get('Nome turma'))
                        
                        disc_idx = disciplinas.index(turma_atual.get('Disciplina')) if turma_atual.get('Disciplina') in disciplinas else 0
                        nova_disciplina = st.selectbox("📚 **Disciplina**", options=disciplinas, index=disc_idx)
                        
                        prof_idx = professores.index(turma_atual.get('Professor')) if turma_atual.get('Professor') in professores else 0
                        novo_professor = st.selectbox("👨‍🏫 **Professor**", options=professores, index=prof_idx)
                        
                        sala_idx = SALA_OPCOES.index(turma_atual.get('Sala')) if turma_atual.get('Sala') in SALA_OPCOES else 0
                        nova_sala = st.selectbox("🚪 **Sala**", options=SALA_OPCOES, index=sala_idx)
                        novo_outro_local = st.text_input("📍 **Especifique o local**", value=turma_atual.get('Outro_Local'), disabled=(nova_sala != "Outro"))
                    with col2:
                        dia_idx = DIAS_SEMANA.index(turma_atual.get('Dia da Semana')) if turma_atual.get('Dia da Semana') in DIAS_SEMANA else 0
                        novo_dia_semana = st.selectbox("🗓️ **Dia da Semana**", options=DIAS_SEMANA, index=dia_idx)

                        try:
                            hora_i = time_obj.fromisoformat(turma_atual.get('Hora de Inicio', '00:00'))
                            hora_f = time_obj.fromisoformat(turma_atual.get('Hora de Fim', '00:00'))
                        except (ValueError, TypeError):
                            hora_i, hora_f = time_obj(9, 0), time_obj(10, 0)
                        
                        nova_hora_inicio = st.time_input("⏰ **Hora de Início**", value=hora_i)
                        nova_hora_fim = st.time_input("🏁 **Hora de Fim**", value=hora_f)
                        novas_vagas = st.number_input("👥 **Número de vagas**", min_value=1, step=1, value=int(turma_atual.get('Numero de vagas', 1)))

                    nivel_idx = NIVEL_OPCOES.index(turma_atual.get('Nivel')) if turma_atual.get('Nivel') in NIVEL_OPCOES else 0
                    novo_nivel = st.selectbox("📶 **Nível**", options=NIVEL_OPCOES, index=nivel_idx)

                    estado_idx = ESTADO_OPCOES.index(turma_atual.get('Estado')) if turma_atual.get('Estado') in ESTADO_OPCOES else 0
                    novo_estado = st.selectbox("📊 **Estado**", options=ESTADO_OPCOES, index=estado_idx)

                    novas_observacoes = st.text_area("📝 **Observações**", value=turma_atual.get('Observacoes', ''))

                    if st.form_submit_button("Guardar Alterações"):
                        erros = []
                        if not novo_nome.strip(): erros.append("Nome da turma é obrigatório.")
                        if nova_disciplina == "-- Selecione --": erros.append("Disciplina é obrigatória.")
                        if novo_professor == "-- Selecione --": erros.append("Professor é obrigatório.")
                        if nova_sala == "Outro" and not novo_outro_local.strip(): erros.append("Especifique o local é obrigatório.")
                        if nova_hora_fim <= nova_hora_inicio: erros.append("A Hora de Fim deve ser posterior à Hora de Início.")

                        if erros:
                            st.error("Por favor, corrija os seguintes erros:\n- " + "\n- ".join(erros))
                        else:
                            conflitos = []
                            for i, turma in df.iterrows():
                                if i == idx: continue # Ignorar a própria turma na verificação
                                if turma.get('Dia da Semana') == novo_dia_semana:
                                    try:
                                        turma_inicio = time_obj.fromisoformat(turma.get('Hora de Inicio'))
                                        turma_fim = time_obj.fromisoformat(turma.get('Hora de Fim'))
                                        if check_time_overlap(nova_hora_inicio, nova_hora_fim, turma_inicio, turma_fim):
                                            if nova_sala != "Outro" and turma.get('Sala') == nova_sala:
                                                conflitos.append(f"Sala '{nova_sala}' já está ocupada neste horário.")
                                            if turma.get('Professor') == novo_professor:
                                                conflitos.append(f"Professor '{novo_professor}' já tem uma aula neste horário.")
                                    except (ValueError, TypeError): continue
                            
                            for i, turma in df.iterrows():
                                if i == idx: continue
                                if normalize_string(turma.get('Nome turma')) == normalize_string(novo_nome) and turma.get('Disciplina') == nova_disciplina:
                                    conflitos.append(f"O nome '{novo_nome}' já existe para a disciplina '{nova_disciplina}'.")
                                    break
                            
                            if conflitos:
                                st.error("Foram encontrados os seguintes conflitos:\n- " + "\n- ".join(conflitos))
                            else:
                                # A coluna A (ID) não é atualizada
                                valores = [
                                    novo_nome, nova_disciplina, novo_professor, nova_sala,
                                    novo_outro_local if nova_sala == "Outro" else "",
                                    novo_dia_semana, nova_hora_inicio.strftime('%H:%M'),
                                    nova_hora_fim.strftime('%H:%M'), novas_vagas,
                                    novo_nivel, novo_estado, novas_observacoes
                                ]
                                sheet_turmas.update(f'B{idx + 2}:M{idx + 2}', [valores])
                                st.success(f"Turma '{novo_nome}' atualizada com sucesso!")
                                del st.session_state['edit_turma_index']
                                time.sleep(0.5)
                                st.rerun()

            # --- VISTA DE APAGAR ---
            elif 'delete_turma_index' in st.session_state:
                idx = st.session_state['delete_turma_index']
                entity_name = df.loc[idx, 'Nome turma'] if 'Nome turma' in df.columns else df.loc[idx].get('Nome da Turma', 'N/A')

                if st.button("⬅️ Voltar à lista"):
                    del st.session_state['delete_turma_index']
                    st.rerun()

                st.subheader("Apagar turma")
                st.warning(f"Tens a certeza que queres apagar a turma: {entity_name}?")
                
                col1, col2, _ = st.columns([1, 1, 5])
                with col1:
                    if st.button("Sim, apagar", type="primary"):
                        sheet_turmas.delete_rows(idx + 2)
                        st.success(f"Turma '{entity_name}' apagada com sucesso!")
                        del st.session_state['delete_turma_index']
                        time.sleep(0.5)
                        st.rerun()
                with col2:
                    if st.button("Cancelar"):
                        del st.session_state['delete_turma_index']
                        st.rerun()

            # --- VISTA DE LISTA ---
            else:
                titulo_secao("Lista de turmas", "📋")
                pesquisa = st.text_input("Pesquisar por nome, disciplina, professor ou sala:")

                if pesquisa:
                    df_filtrado = df[df.apply(lambda row: any(pesquisa.lower() in str(x).lower() for x in row), axis=1)]
                else:
                    df_filtrado = df

                for i, row in df_filtrado.iterrows():
                    expander_title = f"🏫 **{row.get('Nome turma', '')}** ({row.get('Disciplina', '')})"
                    with st.expander(expander_title):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.text_input("🆔 ID", value=row.get('ID_Turma', ''), key=f"disp_id_{i}", disabled=True)
                            st.text_input("👨‍🏫 Professor", value=row.get('Professor', ''), key=f"disp_prof_{i}", disabled=True)
                            sala_display = row.get('Sala', '')
                            if sala_display == "Outro":
                                sala_display = f"Outro: {row.get('Outro_Local', '')}"
                            st.text_input("🚪 Sala", value=sala_display, key=f"disp_sala_{i}", disabled=True)
                            st.text_input("📶 Nível", value=row.get('Nivel', ''), key=f"disp_nivel_{i}", disabled=True)
                        with col2:
                            st.text_input("🗓️ Dia", value=row.get('Dia da Semana', ''), key=f"disp_dia_{i}", disabled=True)
                            st.text_input("⏰ Horário", value=f"{row.get('Hora de Inicio', '')} - {row.get('Hora de Fim', '')}", key=f"disp_hora_{i}", disabled=True)
                            st.text_input("👥 Vagas", value=str(row.get('Numero de vagas', '')), key=f"disp_vagas_{i}", disabled=True)
                            st.text_input("📊 Estado", value=row.get('Estado', ''), key=f"disp_estado_{i}", disabled=True)
                        
                        st.text_area("📝 Observações", value=row.get('Observacoes', ''), key=f"disp_obs_{i}", disabled=True)

                        st.write("---")
                        b_col1, b_col2, _ = st.columns([1, 1, 5])
                        with b_col1:
                            if st.button("✏️ Editar", key=f"edit_turma_{i}", use_container_width=True):
                                st.session_state['edit_turma_index'] = i
                                st.rerun()
                        with b_col2:
                            if st.button("🗑️ Apagar", key=f"delete_turma_{i}", use_container_width=True):
                                st.session_state['delete_turma_index'] = i
                                st.rerun()
