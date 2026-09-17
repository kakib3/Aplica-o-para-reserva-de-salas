"""
Componentes de UI reutilizaveis relacionados a salas e reservas.
Sem logica de negocio - apenas renderizacao (Streamlit widgets).
"""
import streamlit as st

from app.services.reservas import cancelar_reserva
from app.services.validacao import RegraNegocioError, STATUS_RESERVA_CONFIRMADA

CORES_STATUS_SALA = {
    "Disponivel": "🟢",
    "Manutencao": "🟠",
    "Indisponivel": "🔴",
}


def render_card_sala(sala, on_ver_detalhes=None):
    """
    Renderiza um card com as informacoes de uma sala.

    sala: dict com os dados da sala (idSala, nome, predio, andar, capacidade, status, descricao)
    on_ver_detalhes: funcao chamada com o idSala quando o botao "Ver detalhes" e clicado
    """
    with st.container(border=True):
        col_info, col_status, col_acao = st.columns([3, 1, 1])

        with col_info:
            st.markdown(f"### {sala['nome']}")
            st.write(f"📍 {sala['predio']} - {sala['andar']}º andar")
            st.write(f"👥 Capacidade: {sala['capacidade']} pessoas")
            if sala.get("descricao"):
                st.caption(sala["descricao"])

        with col_status:
            cor = CORES_STATUS_SALA.get(sala["status"], "⚪")
            st.metric("Status", f"{cor} {sala['status']}")

        with col_acao:
            if st.button("Ver detalhes", key=f"ver_{sala['idSala']}"):
                if on_ver_detalhes:
                    on_ver_detalhes(sala["idSala"])


def render_card_reserva(reserva, nome_sala, id_usuario):
    """
    Renderiza um card com as informacoes de uma reserva, com botao de cancelar.

    reserva: dict com os dados da reserva (idReserva, data, horaInicio, horaFim, status)
    nome_sala: nome da sala ja resolvido (string)
    id_usuario: id do usuario logado, usado para validar o cancelamento
    """
    with st.container(border=True):
        col_info, col_status, col_acao = st.columns([3, 1, 1])

        with col_info:
            st.markdown(f"### {nome_sala}")
            st.write(f"📅 {reserva['data']} 🕐 {reserva['horaInicio']} - {reserva['horaFim']}")

        with col_status:
            cor = "🟢" if reserva["status"] == STATUS_RESERVA_CONFIRMADA else "🔴"
            st.metric("Status", f"{cor} {reserva['status']}")

        with col_acao:
            st.button(
                "Alterar",
                disabled=True,
                key=f"alterar_{reserva['idReserva']}",
                help="Indisponível: aguardando implementação de alterar_reserva() no back-end"
            )
            if reserva["status"] == STATUS_RESERVA_CONFIRMADA:
                if st.button("Cancelar", key=f"cancelar_{reserva['idReserva']}"):
                    try:
                        cancelar_reserva(reserva["idReserva"], id_usuario)
                        st.success("Reserva cancelada com sucesso.")
                        st.rerun()
                    except RegraNegocioError as erro:
                        st.error(f"Não foi possível cancelar: {erro}")
            else:
                st.button(
                    "Cancelar",
                    disabled=True,
                    key=f"cancelar_disabled_{reserva['idReserva']}"
                )