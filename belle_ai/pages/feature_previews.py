import streamlit as st

from belle_ai.ui import render_empty_state


def render_image_analysis() -> None:
    st.markdown(
        '<div class="feature-label">PREVIEW ONLY · NO AI INTERPRETATION</div>',
        unsafe_allow_html=True,
    )
    st.write("")
    st.markdown(
        "Choose an image to preview it in this app session. It will not be sent to an AI service."
    )
    image = st.file_uploader(
        "Choose an image",
        type=["png", "jpg", "jpeg", "webp"],
        accept_multiple_files=False,
        key="image_preview_upload",
    )
    if image:
        st.image(image, caption=image.name, use_container_width=True)
        st.info("Preview only. The image is not interpreted or sent to an AI service.")
    else:
        render_empty_state(
            "Image analysis is not connected",
            "Gemini-based image interpretation is planned for a later phase. For now, you can preview a selected image locally.",
        )


def render_knowledge_graph() -> None:
    st.markdown(
        '<div class="feature-label">PLANNED · NOT ACTIVE</div>',
        unsafe_allow_html=True,
    )
    st.write("")
    render_empty_state(
        "Your research map will grow here",
        "Knowledge graph generation is not implemented yet. This preview does not infer or display connections between documents.",
    )
    st.write("")
    st.caption("NetworkX visualization and document connections are planned for a later phase.")
