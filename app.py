
import streamlit as st

from belle_ai.pages.dashboard import render_dashboard
from belle_ai.pages.documents import render_documents
from belle_ai.pages.feature_previews import render_image_analysis
from belle_ai.pages.research_chat import (
    render_research_chat,
    groq_is_configured,
)
from belle_ai.pages.settings import render_settings
from belle_ai.ui import (
    PAGE_DETAILS,
    inject_styles,
    render_page_header,
)


st.set_page_config(
    page_title="belleAI — Research workspace",
    page_icon="B",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Available pages — Knowledge Graph removed.
AVAILABLE_PAGES = [
    "Dashboard",
    "My Documents",
    "Research Chat",
    "Image Analysis",
    "Settings",
]

# Initialize session state.
st.session_state.setdefault("active_page", "Dashboard")
st.session_state.setdefault("documents", {})
st.session_state.setdefault("upload_version", 0)
st.session_state.setdefault("upload_feedback", [])

# Handle an old session that was on Knowledge Graph.
if st.session_state["active_page"] not in AVAILABLE_PAGES:
    st.session_state["active_page"] = "Dashboard"

inject_styles()

# Detect which AI service is configured.
if groq_is_configured():
    ai_status_title = "Groq AI"
    ai_status_message = "Connected · GPT-OSS 20B"
    ai_status_color = "#22c55e"
else:
    ai_status_title = "Local AI"
    ai_status_message = "Ollama · Local connection required"
    ai_status_color = "#f59e0b"

with st.sidebar:
    st.markdown(
        """
        <div class="brand-lockup">
          <div class="brand-mark">b</div>
          <div>
            <div class="brand-name">belle<span>AI</span></div>
            <div class="brand-caption">RESEARCH WORKSPACE</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-section-label">WORKSPACE</div>',
        unsafe_allow_html=True,
    )

    st.radio(
        "Workspace pages",
        options=AVAILABLE_PAGES,
        key="active_page",
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown(
        f"""
        <div class="sidebar-status">
          <div class="sidebar-status-title">
            <span
              class="status-dot"
              style="background-color: {ai_status_color};"
            ></span>
            {ai_status_title}
          </div>
          <div class="sidebar-status-copy">
            {ai_status_message}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption("Your PDFs stay in this app session.")

# Render the selected page.
page = st.session_state["active_page"]

title, subtitle, eyebrow = PAGE_DETAILS[page]

render_page_header(
    title=title,
    subtitle=subtitle,
    eyebrow=eyebrow,
)

if page == "Dashboard":
    render_dashboard()

elif page == "My Documents":
    render_documents()

elif page == "Research Chat":
    render_research_chat()

elif page == "Image Analysis":
    render_image_analysis()

elif page == "Settings":
    render_settings()

else:
    st.warning("This page is not available.")
