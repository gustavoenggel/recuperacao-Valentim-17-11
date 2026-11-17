"""
frontend.py
Interface Streamlit que exibe os dados meteorológicos obtidos pelo consumidor.
Execução: python -m streamlit run frontend.py
"""

import streamlit as st

from consumidor import ErroConsumidorAPI, obter_dados_meteorologicos

st.set_page_config(page_title="Monitoramento Meteorológico", page_icon="🌦️", layout="wide")

st.title("🌦️ Monitoramento Meteorológico")
st.caption("Jaraguá do Sul — SC | Dados da API Meteorológica Offline (simulados)")
st.divider()

# Botão que recarrega a página e consulta a API novamente
if st.button("🔄 Atualizar dados"):
    st.rerun()

try:
    with st.spinner("Consultando a API meteorológica..."):
        dados = obter_dados_meteorologicos()

    un = dados["unidades"]
    st.success("Dados meteorológicos carregados.")
    st.subheader("Condições atuais")

    # Primeira linha de indicadores
    col1, col2, col3 = st.columns(3)
    col1.metric("🌡️ Temperatura do ar", f"{dados['temperatura']} {un['temperatura']}")
    col2.metric("💧 Umidade relativa", f"{dados['umidade_relativa']} {un['umidade_relativa']}")
    col3.metric("🥵 Sensação térmica", f"{dados['sensacao_termica']} {un['sensacao_termica']}")

    # Segunda linha de indicadores
    col4, col5, col6 = st.columns(3)
    col4.metric("🌧️ Precipitação", f"{dados['precipitacao']} {un['precipitacao']}")
    col5.metric("💨 Velocidade do vento", f"{dados['velocidade_vento']} {un['velocidade_vento']}")

except ErroConsumidorAPI as erro:
    # Falhas previstas: mensagem clara, sem confundir com dados meteorológicos
    st.error(f"Falha ao obter os dados: {erro}")
except Exception as erro:
    st.error(f"Erro inesperado na aplicação: {erro}")