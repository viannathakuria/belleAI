
import base64
import os

import streamlit as st
from groq import Groq

from belle_ai.ui import render_empty_state


def render_image_analysis() -> None:
    st.markdown(
        '<div class="feature-label">AI-POWERED IMAGE ANALYSIS</div>',
        unsafe_allow_html=True,
    )
    st.write("")
    st.markdown(
        "Upload an image and ask belleAI a question about it. "
        "AI can help explain charts, diagrams, screenshots, and other visuals."
    )

    image = st.file_uploader(
        "Choose an image",
        type=["png", "jpg", "jpeg", "webp"],
        accept_multiple_files=False,
        key="image_preview_upload",
    )

    if image is None:
        render_empty_state(
            "Ready to analyze your image",
            "Upload a PNG, JPG, or WEBP image to get started.",
        )
        return

    st.image(image, caption=image.name, use_container_width=True)

    question = st.text_area(
        "What would you like to know about this image?",
        placeholder="Explain this image in simple terms.",
        key="image_analysis_question",
    )

    if st.button(
        "Analyze image",
        type="primary",
        use_container_width=True,
        key="analyze_image_button",
    ):
        if not question.strip():
            st.warning("Please enter a question first.")
            return

        try:
            api_key = st.secrets.get("GROQ_API_KEY") or os.getenv(
                "GROQ_API_KEY"
            )
        except Exception:
            api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            st.error(
                "Groq API key not found. Add GROQ_API_KEY to "
                "your Streamlit secrets."
            )
            return

        image_bytes = image.getvalue()

        if len(image_bytes) > 4 * 1024 * 1024:
            st.error(
                "This image is too large. Please use an image under 4 MB."
            )
            return

        mime_type = image.type or "image/png"
        encoded_image = base64.b64encode(image_bytes).decode("utf-8")
        image_url = f"data:{mime_type};base64,{encoded_image}"

        with st.spinner("belleAI is analyzing your image..."):
            try:
                client = Groq(api_key=api_key)

                response = client.chat.completions.create(
                    model="qwen/qwen3.8-27b",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are belleAI, a helpful research assistant. "
                                "Analyze the provided image and answer the user's "
                                "question clearly and accurately. "
                                "If the image contains a chart or diagram, "
                                "explain the visible information. "
                                "Do not invent details that are not visible."
                            ),
                        },
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": question,
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": image_url
                                    },
                                },
                            ],
                        },
                    ],
                    temperature=0.2,
                    max_completion_tokens=1024,
                )

                answer = response.choices[0].message.content

                st.markdown("### belleAI's Analysis")
                st.write(answer or "No analysis was returned.")

            except Exception as error:
                st.error(f"Image analysis failed: {error}")


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
    st.caption(
        "NetworkX visualization and document connections are planned for a later phase.")
