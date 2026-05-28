import pandas as pd
import streamlit as st

from database.init_db import init_db
from repositories.cronogramas import (
    buscar_ultimo_cronograma,
    excluir_cronograma,
    listar_itens_cronograma,
)
from services.cronograma_service import gerar_cronograma_automatico
from services.pdf_service import gerar_pdf_cronograma
from utils.session import mostrar_sidebar_usuario, require_login

st.set_page_config(page_title="Cronograma", page_icon="🗓️", layout="wide")

init_db()
usuario = require_login()
mostrar_sidebar_usuario()

st.title("🗓️ Cronograma semanal")
st.write("Gere automaticamente seu cronograma com base nas disciplinas, atividades e horários livres.")

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("Gerar / Recalcular cronograma", type="primary"):
        ok, mensagem, _ = gerar_cronograma_automatico(usuario["id"])
        if ok:
            st.success(mensagem)
            st.rerun()
        else:
            st.error(mensagem)

ultimo = buscar_ultimo_cronograma(usuario["id"])

if not ultimo:
    st.info("Nenhum cronograma foi gerado ainda.")
    st.stop()

itens = listar_itens_cronograma(usuario["id"], ultimo["id"])

with col2:
    if st.button("Excluir cronograma atual"):
        try:
            excluir_cronograma(usuario["id"], ultimo["id"])
            st.success("Cronograma excluído com sucesso.")
            st.rerun()
        except Exception as exc:
            st.error(f"Erro ao excluir cronograma: {exc}")

st.markdown(f"### Último cronograma gerado em: {ultimo['data_criacao']}")

if not itens:
    st.warning("O cronograma atual não possui itens.")
    st.stop()

df = pd.DataFrame(itens)
df["hora_inicio"] = df["hora_inicio"].astype(str).str.slice(0, 5)
df["hora_fim"] = df["hora_fim"].astype(str).str.slice(0, 5)

df_exibicao = df[["dia_semana", "hora_inicio", "hora_fim", "descricao"]].rename(
    columns={
        "dia_semana": "Dia",
        "hora_inicio": "Início",
        "hora_fim": "Fim",
        "descricao": "Atividade planejada",
    }
)

st.dataframe(df_exibicao, use_container_width=True, hide_index=True)

pdf_bytes = gerar_pdf_cronograma(usuario, ultimo, itens)

st.download_button(
    label="Baixar cronograma em PDF",
    data=pdf_bytes,
    file_name="cronograma_organizaai.pdf",
    mime="application/pdf",
)
