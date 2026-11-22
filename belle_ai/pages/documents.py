from __future__ import annotations

from datetime import datetime
from html import escape

import streamlit as st

from belle_ai.document_processing import (
    PDFProcessingError,
    document_id,
    extract_pdf_text,
)
from belle_ai.ui import format_bytes, render_empty_state


def _remove_document(doc_id: str) -> None:
    st.session_state["documents"].pop(doc_id, None)
    st.session_state["upload_version"] += 1


def _handle_uploads(uploaded_files: list) -> None:
    documents = st.session_state["documents"]
    feedback: list[tuple[str, str]] = []
    added_count = 0

    for uploaded_file in uploaded_files:
        pdf_bytes = uploaded_file.getvalue()
        doc_id = document_id(pdf_bytes)
        if doc_id in documents:
            continue

        try:
            text, page_count = extract_pdf_text(pdf_bytes)
        except PDFProcessingError as error:
            feedback.append(
                ("error", f"{uploaded_file.name}: {error}")
            )
            continue

        documents[doc_id] = {
            "name": uploaded_file.name,
            "text": text,
            "page_count": page_count,
            "size_bytes": len(pdf_bytes),
            "added_at": datetime.now().isoformat(timespec="seconds"),
        }
        added_count += 1
        if text:
            feedback.append(("success", f"Added {uploaded_file.name}."))
        else:
            feedback.append(
                (
                    "warning",
                    f"Added {uploaded_file.name}, but no selectable text was found. "
                    "It may contain scanned pages; OCR is not available yet.",
                )
            )

    if feedback:
        st.session_state["upload_feedback"] = feedback
    if added_count:
        st.session_state["upload_version"] += 1
        st.rerun()


def render_documents() -> None:
    documents = st.session_state["documents"]
    st.markdown("### Add research documents")
    st.markdown(
        '<p class="section-intro">PDFs are processed in your session. belleAI extracts selectable text and does not upload files to an AI service.</p>',
        unsafe_allow_html=True,
    )

    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        key=f"pdf_upload_{st.session_state['upload_version']}",
        max_upload_size=50,
        help="PDF files up to 50 MB each. Password-protected files cannot be read.",
    )
    if uploaded_files:
        _handle_uploads(uploaded_files)

    feedback = st.session_state.pop("upload_feedback", [])
    for level, message in feedback:
        getattr(st, level)(message)

    st.write("")
    st.markdown("### Your library")
    if not documents:
        render_empty_state(
            "No documents yet",
            "Choose a PDF above to begin. Your files and extracted text stay in this session and are cleared when it ends.",
        )
        return

    ordered_documents = sorted(
        documents.items(),
        key=lambda item: item[1].get("added_at", ""),
        reverse=True,
    )
    st.caption(
        f"{len(ordered_documents)} "
        f"{'document' if len(ordered_documents) == 1 else 'documents'} in this session"
    )

    for doc_id, document in ordered_documents:
        with st.container(border=True):
            details, actions = st.columns([5, 1.1], vertical_alignment="center")
            with details:
                st.markdown(
                    f'<div class="document-name">{escape(document["name"])}</div>',
                    unsafe_allow_html=True,
                )
                st.caption(
                    f"{document['page_count']} pages · "
                    f"{format_bytes(document['size_bytes'])} · "
                    f"{len(document['text'].split()):,} words extracted"
                )
            with actions:
                st.button(
                    "Remove",
                    key=f"remove_{doc_id}",
                    on_click=_remove_document,
                    args=(doc_id,),
                    use_container_width=True,
                )

            with st.expander("View extracted text"):
                if document["text"]:
                    st.text_area(
                        "Extracted text",
                        value=document["text"],
                        height=280,
                        disabled=True,
                        key=f"text_{doc_id}",
                        label_visibility="collapsed",
                    )
                else:
                    st.info(
                        "No selectable text was found in this PDF. Scanned-page OCR is not included yet."
                    )
