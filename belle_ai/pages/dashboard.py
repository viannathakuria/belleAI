
from __future__ import annotations

from belle_ai.ui import format_bytes, navigate_to, render_empty_state
import streamlit as st


def render_dashboard() -> None:
    documents = list(st.session_state["documents"].values())
    total_pages = sum(document["page_count"] for document in documents)
    total_words = sum(len(document["text"].split()) for document in documents)

    st.markdown("### Your library at a glance")
    st.markdown(
        '<p class="section-intro">A calm overview of what you have collected in this session.</p>',
        unsafe_allow_html=True,
    )

    metrics = st.columns(3)
    metric_values = [
        ("Documents", len(documents)),
        ("Pages", total_pages),
        ("Words extracted", f"{total_words:,}"),
    ]
    for column, (label, value) in zip(metrics, metric_values):
        with column:
            with st.container(border=True):
                st.metric(label, value)

    st.write("")
    left, right = st.columns([1.2, 0.8], gap="large")
    with left:
        with st.container(border=True):
            st.markdown("#### Recent documents")
            if not documents:
                render_empty_state(
                    "Your library is ready",
                    "Upload a PDF to see its name, page count, and extracted text here.",
                )
                st.write("")
                st.button(
                    "Add your first document",
                    key="dashboard_add_document",
                    on_click=navigate_to,
                    args=("My Documents",),
                    type="primary",
                )
            else:
                recent = sorted(
                    documents,
                    key=lambda item: item.get("added_at", ""),
                    reverse=True,
                )[:5]
                for document in recent:
                    st.markdown(
                        f"**{document['name']}**  \n"
                        f"{document['page_count']} pages · {format_bytes(document['size_bytes'])}"
                    )
                    st.divider()
                st.button(
                    "Open document library",
                    key="dashboard_open_library",
                    on_click=navigate_to,
                    args=("My Documents",),
                )

    with right:
        with st.container(border=True):
            st.markdown("#### Explore belleAI")
            st.markdown(
                "Your document library is ready. Use Research Chat to ask questions about your uploaded PDFs."
            )
            st.write("")
            st.markdown("**Research Chat**")
            st.caption(
                "Ask questions about your documents and get AI-generated answers with page citations."
            )
            st.button(
                "Open Research Chat",
                key="dashboard_open_chat",
                on_click=navigate_to,
                args=("Research Chat",),
                use_container_width=True,
            )
            st.markdown("**Image Analysis · Knowledge Graph**")
            st.caption(
                "These pages explain what is planned and what is not active.")
