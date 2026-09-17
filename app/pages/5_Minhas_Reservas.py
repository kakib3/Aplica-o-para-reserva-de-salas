import streamlit as st

from app.services.reservas import (
    listar_reservas_por_usuario,
    cancelar_reserva
)
from app.services.salas import buscar_sala_por_id
from app.services.validacao import (
    RegraNegocioError,
    STATUS_RESERVA_CONFIRMADA
)
from app.utils.session import exigir_usuario_selecionado
from app.components.cards import render_card_reserva

st.set_page_config(
    page_title="Minhas Reservas - UNISAPIENS",
    page_icon="🗂️",
    layout="wide"
)

usuario_atual = exigir_usuario_selecionado()

st.title("🗂️ Minhas Reservas")
st.caption(
    f"Usuário: {usuario_atual['nome']} "
    f"(id {usuario_atual['idUser']}, {usuario_atual['role']})"
)

df_reservas = listar_reservas_por_usuario(
    usuario_atual["idUser"]
)

if df_reservas.empty:
    st.info("Você ainda não possui reservas.")
    st.stop()

if "criado_em" in df_reservas.columns:
    df_reservas = df_reservas.sort_values(
        "criado_em",
        ascending=False
    )

st.divider()

for _, reserva in df_reservas.iterrows():
    sala = buscar_sala_por_id(reserva["idSala"])
    nome_sala = sala["nome"] if sala else f"Sala #{reserva['idSala']}"
    render_card_reserva(reserva, nome_sala, usuario_atual["idUser"])