import streamlit as st


def render_settings() -> None:
    with st.container(border=True):
        st.markdown("#### Session and storage")
        st.markdown(
            "Uploaded PDFs and extracted text are held in memory for this Streamlit session only."
        )
        st.caption(
            "They are not saved to disk, sent to an AI provider, or retained after the session ends."
        )

    st.write("")
    with st.container(border=True):
        st.markdown("#### Integrations")
        st.markdown("**Gemini API**")
        st.caption("Not connected — research chat and AI image analysis are inactive.")
        st.divider()
        st.markdown("**FAISS · NetworkX**")
        st.caption("Not enabled — vector search and knowledge graph features are planned.")

    st.write("")
    st.info(
        "This first release does not ask for API keys and does not call paid external services."
    )
