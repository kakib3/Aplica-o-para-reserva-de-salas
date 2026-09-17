"""
Componentes de UI reutilizaveis relacionados a salas.
Sem logica de negocio - apenas renderizacao (Streamlit widgets).
"""
import streamlit as st

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