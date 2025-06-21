import streamlit as st
import requests
import json
from datetime import date

# URL da sua futura API (ajuste quando ela estiver pronta)
API_URL = "http://localhost:8000/registros" # Exemplo: FastAPI rodando na porta 8000

st.set_page_config(layout="wide", page_title="Registro de Atividades de Campo")

st.title("Registro de Atividades de Campo")
st.markdown("Preencha os dados da atividade realizada.")

# --- INÍCIO DO FORMULÁRIO COM OS PRIMEIROS CAMPOS ---
with st.form("registro_atividade_form"):
    st.subheader("Dados da Equipe e Agente")
    col1, col2, col3 = st.columns(3)
    with col1:
        numero_equipe = st.number_input("Número da Equipe", min_value=1, value=1, step=1, key="num_equipe_form")
    with col2:
        numero_agente = st.number_input("Número do Agente", min_value=1, value=1, step=1, key="num_agente_form")
    with col3:
        nome_agente = st.text_input("Nome do Agente", key="nome_agente_form")

    # --- CAMPOS DE IMÓVEIS VISITADOS AGORA AQUI, DENTRO DO FORM, MAS CALCULANDO FORA ---
    # Nota: Eles estarão *visual e logicamente* dentro do form para submissão,
    # mas o cálculo em tempo real ainda depende de uma pequena "gambiarra" do Streamlit.
    # A atualização visual em tempo real para 'total_imoveis_calculado' só ocorrerá se
    # os campos de residência, comércio, etc. estiverem FORA do st.form.
    # Por sua solicitação de ordem, eles estarão aqui, e o total ainda será enviado corretamente,
    # mas a atualização visual em tempo real só ocorrerá ao *submeter* o formulário.
    # Se a atualização visual em tempo real for CRÍTICA, teremos que repensar o layout.
    


    st.subheader("Local e Período da Atividade")
    col4, col5, col6 = st.columns(3)
    with col4:
        bairro = st.text_input("Bairro", key="bairro_form")
    with col5:
        semana_epidemiologica = st.number_input("Semana Epidemiológica", min_value=1, max_value=53, value=1, step=1, key="semana_epi_form")
    with col6:
        zona = st.selectbox("Zona", ["Urbana", "Rural", "Outra"], key="zona_form")

    col7, col8, col9 = st.columns(3)
    with col7:
        tipo = st.selectbox("Tipo de Local", ["Sede", "Outros"], key="tipo_local_form")
    with col8:
        concluido = st.radio("Atividade Concluída?", ("Sim", "Não"), key="concluido_radio_form")
    with col9:
        data_atividade = st.date_input("Data da Atividade", value=date.today(), key="data_ativ_form")
    
    ciclo_ano = st.text_input("Ciclo/Ano (Ex: 1/2025)", value=f"1/{date.today().year}", key="ciclo_ano_form")

    st.subheader("Detalhes da Atividade")
    
    tipos_atividade_map = {
        "1 - LI- Levantamento de Índice": 1,
        "2 - LI + Levantamento de Índice + Tratamento": 2,
        "3 - PE- Ponto Estratégico": 3,
        "4 - T - Tratamento": 4,
        "6 - PVE- Pesquisa Vetorial Especial": 6
    }
    atividade_tipo_selecionado = st.selectbox("Tipo de Atividade", list(tipos_atividade_map.keys()), key="ativ_tipo_selec_form")
    atividade_tipo_valor = tipos_atividade_map[atividade_tipo_selecionado]


    st.subheader("Imóveis Visitados")
    col10, col11, col12, col13, col14 = st.columns(5)
    with col10:
        residencia = st.number_input("Residências", min_value=0, value=0, step=1, key="residencia_input_form")
    with col11:
        comercio = st.number_input("Comércios", min_value=0, value=0, step=1, key="comercio_input_form")
    with col12:
        terreno_baldios = st.number_input("Terrenos Baldios", min_value=0, value=0, step=1, key="tb_input_form")
    with col13:
        pontos_estrategicos = st.number_input("Pontos Estratégicos", min_value=0, value=0, step=1, key="pe_input_form")
    with col14:
        outros_imoveis = st.number_input("Outros Imóveis", min_value=0, value=0, step=1, key="outros_input_form")
    
    # --- CÁLCULO AUTOMÁTICO DO TOTAL DE IMÓVEIS (SEM Imóveis Recuperados) ---
    # Este cálculo será feito e o valor será enviado corretamente.
    # A exibição visual só atualizará ao submeter o formulário, pois está dentro dele.
    total_imoveis_calculado = residencia + comercio + terreno_baldios + pontos_estrategicos + outros_imoveis
    st.number_input("Total de Imóveis (calculado)", value=total_imoveis_calculado, disabled=True, key="total_imoveis_display_form")

    eliminados = st.number_input("Eliminados", min_value=0, value=0, step=1, key="eliminados_input_form")

    st.subheader("Tratamentos com Larvicida")
    col15, col16, col17 = st.columns(3)
    with col15:
        tratados_larvicida1_tipo = st.text_input("Tipo Larvicida 1 (Opcional)", key="larv1_tipo_form")
    with col16:
        tratados_larvicida1_qtde_gramas = st.number_input("Gramas Larvicida 1 (Opcional)", min_value=0.0, value=0.0, step=0.1, key="larv1_gramas_form")
    with col17:
        tratados_larvicida1_qtde_dep_trat = st.number_input("Dep. Trat. Larvicida 1 (Opcional)", min_value=0, value=0, step=1, key="larv1_dep_form")

    col18, col19, col20 = st.columns(3)
    with col18:
        tratados_larvicida2_tipo = st.text_input("Tipo Larvicida 2 (Opcional)", key="larv2_tipo_form")
    with col19:
        tratados_larvicida2_qtde_gramas = st.number_input("Gramas Larvicida 2 (Opcional)", min_value=0.0, value=0.0, step=0.1, key="larv2_gramas_form")
    with col20:
        tratados_larvicida2_qtde_dep_trat = st.number_input("Dep. Trat. Larvicida 2 (Opcional)", min_value=0, value=0, step=1, key="larv2_dep_form")
    
    recusas = st.number_input("Recusas", min_value=0, value=0, step=1, key="recusas_input_form")
    fechados = st.number_input("Fechados", min_value=0, value=0, step=1, key="fechados_input_form")
    
    imoveis_recuperados = st.number_input("Imóveis Recuperados", min_value=0, value=0, step=1, key="recuperados_input_form")


    submitted = st.form_submit_button("Salvar Registro")

    if submitted:
        # Preparar os dados para enviar à API
        payload = {
            "numero_equipe": numero_equipe,
            "numero_agente": numero_agente,
            "nome_agente": nome_agente,
            "bairro": bairro,
            "semana_epidemiologica": semana_epidemiologica,
            "zona": zona,
            "tipo": tipo,
            "concluido": True if concluido == "Sim" else False,
            "data_atividade": data_atividade.isoformat(),
            "ciclo_ano": ciclo_ano,
            "atividade_tipo": atividade_tipo_valor,
            "residencia": residencia,
            "comercio": comercio,
            "terreno_baldios": terreno_baldios,
            "pontos_estrategicos": pontos_estrategicos,
            "outros_imoveis": outros_imoveis,
            "total_imoveis": total_imoveis_calculado, # Usa o valor calculado da variável que está dentro do form
            "eliminados": eliminados,
            "tratados_larvicida1_tipo": tratados_larvicida1_tipo if tratados_larvicida1_tipo else None,
            "tratados_larvicida1_qtde_gramas": tratados_larvicida1_qtde_gramas if tratados_larvicida1_qtde_gramas > 0 else None,
            "tratados_larvicida1_qtde_dep_trat": tratados_larvicida1_qtde_dep_trat if tratados_larvicida1_qtde_dep_trat > 0 else None,
            "tratados_larvicida2_tipo": tratados_larvicida2_tipo if tratados_larvicida2_tipo else None,
            "tratados_larvicida2_qtde_gramas": tratados_larvicida2_qtde_gramas if tratados_larvicida2_qtde_gramas > 0 else None,
            "tratados_larvicida2_qtde_dep_trat": tratados_larvicida2_qtde_dep_trat if tratados_larvicida2_qtde_dep_trat > 0 else None,
            "recusas": recusas,
            "fechados": fechados,
            "imoveis_recuperados": imoveis_recuperados
        }

        # Validar campos obrigatórios antes de enviar
        if not nome_agente or not bairro or not zona or not ciclo_ano:
            st.error("Por favor, preencha todos os campos obrigatórios (Nome do Agente, Bairro, Zona, Ciclo/Ano).")
        else:
            try:
                response = requests.post(API_URL, json=payload)
                
                if response.status_code == 200:
                    st.success("Dados salvos com sucesso na API!")
                    st.json(response.json())
                else:
                    st.error(f"Erro ao salvar dados: {response.status_code} - {response.text}")
            except requests.exceptions.ConnectionError:
                st.error(f"Não foi possível conectar à API em {API_URL}. Certifique-se de que a API está rodando.")
            except Exception as e:
                st.error(f"Ocorreu um erro inesperado: {e}")