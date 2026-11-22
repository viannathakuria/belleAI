
from __future__ import annotations

from html import escape

import streamlit as st


PAGE_DETAILS = {
    "Dashboard": (
        "Your research, in focus",
        "A clear starting point for the papers and ideas you are exploring.",
        "OVERVIEW",
    ),
    "My Documents": (
        "My Documents",
        "Add research PDFs, review extracted text, and keep your session organized.",
        "YOUR LIBRARY",
    ),
    "Research Chat": (
        "Research Chat",
        "Ask questions, explore ideas, and get answers grounded in your uploaded PDFs.",
        "ASSISTANT",
    ),
    "Image Analysis": (
        "Image Analysis",
        "Image interpretation is not connected yet. You can preview an image locally.",
        "MULTIMODAL",
    ),
    "Knowledge Graph": (
        "Knowledge Graph",
        "A visual map of connections will be available in a later phase.",
        "DISCOVERY",
    ),
    "Settings": (
        "Settings",
        "See how this workspace handles documents and which capabilities are connected.",
        "PREFERENCES",
    ),
}


def groq_is_configured() -> bool:
    """Check whether a Groq API key is available."""
    try:
        return bool(st.secrets.get("GROQ_API_KEY"))
    except Exception:
        return False


def inject_styles() -> None:
    """Apply the belleAI visual theme to Streamlit's built-in UI."""
    st.markdown(
        """
        <style>
          :root {
            --ink: #17213d;
            --muted: #68728c;
            --line: #e6e9f2;
            --lavender: #7767d8;
            --lavender-soft: #f0edff;
            --surface: #ffffff;
          }
          .stApp {
            background: #f7f8fc;
            color: var(--ink);
            font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
          }
          [data-testid="stHeader"] {
            background: rgba(247, 248, 252, 0.92);
          }
          [data-testid="stAppViewContainer"] > .main .block-container {
            max-width: 1480px;
            padding: 2rem 3rem 4rem;
          }
          [data-testid="stSidebar"] {
            background: #fff;
            border-right: 1px solid var(--line);
          }
          [data-testid="stSidebar"] > div:first-child {
            padding-top: 1.6rem;
          }
          .brand-lockup {
            display: flex;
            gap: 0.75rem;
            align-items: center;
            padding: 0.25rem 0.15rem 1.7rem;
          }
          .brand-mark {
            display: grid;
            width: 2.65rem;
            height: 2.65rem;
            place-items: center;
            border-radius: 0.9rem;
            background: linear-gradient(145deg, #252f55, #6256b5);
            color: #fff;
            font-size: 1.55rem;
            font-weight: 700;
            line-height: 1;
          }
          .brand-name {
            color: #202a48;
            font-size: 1.17rem;
            font-weight: 720;
            letter-spacing: -0.045em;
          }
          .brand-name span { color: var(--lavender); }
          .brand-caption {
            margin-top: 0.16rem;
            color: #8a92a8;
            font-size: 0.58rem;
            font-weight: 700;
            letter-spacing: 0.14em;
          }
          .sidebar-section-label {
            margin: 0.5rem 0 0.45rem 0.45rem;
            color: #9299ab;
            font-size: 0.64rem;
            font-weight: 700;
            letter-spacing: 0.13em;
          }
          [data-testid="stSidebar"] [role="radiogroup"] { gap: 0.22rem; }
          [data-testid="stSidebar"] [role="radiogroup"] label {
            min-height: 2.65rem;
            padding: 0.45rem 0.65rem;
            border-radius: 0.7rem;
            color: #58627b;
            font-size: 0.9rem;
            transition: background 140ms ease, color 140ms ease;
          }
          [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
            background: var(--lavender-soft);
            color: #5143aa;
            font-weight: 650;
          }
          [data-testid="stSidebar"] [role="radiogroup"] label > div:first-child {
            display: none;
          }
          .sidebar-status {
            margin: 0.5rem 0 0.35rem;
            padding: 0.9rem 0.85rem;
            border: 1px solid var(--line);
            border-radius: 0.8rem;
            background: #fbfbfe;
          }
          .sidebar-status-title {
            display: flex;
            align-items: center;
            gap: 0.45rem;
            color: #303a56;
            font-size: 0.79rem;
            font-weight: 650;
          }
          .status-dot {
            width: 0.45rem;
            height: 0.45rem;
            border-radius: 50%;
            background: #b9bfd0;
          }
          .sidebar-status-copy {
            margin: 0.35rem 0 0 0.9rem;
            color: #8790a5;
            font-size: 0.75rem;
          }
          .page-heading {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 1rem;
            margin: 0.1rem 0 2rem;
          }
          .page-eyebrow {
            margin: 0 0 0.45rem;
            color: #786bc6;
            font-size: 0.67rem;
            font-weight: 750;
            letter-spacing: 0.14em;
          }
          .page-title {
            margin: 0;
            color: #182341;
            font-size: clamp(1.7rem, 3vw, 2.35rem);
            font-weight: 720;
            letter-spacing: -0.055em;
            line-height: 1.14;
          }
          .page-subtitle {
            margin: 0.62rem 0 0;
            color: #707991;
            font-size: 0.96rem;
            line-height: 1.55;
          }
          .connection-badge {
            display: flex;
            flex: 0 0 auto;
            align-items: center;
            gap: 0.48rem;
            margin-top: 0.25rem;
            padding: 0.52rem 0.75rem;
            border: 1px solid #e7e8f1;
            border-radius: 999px;
            background: #fff;
            color: #6b748b;
            font-size: 0.74rem;
            font-weight: 600;
          }
          .badge-dot {
            width: 0.42rem;
            height: 0.42rem;
            border-radius: 50%;
            background: #c1c5d0;
          }
          .section-intro {
            margin: -0.75rem 0 1.35rem;
            color: #737c93;
            font-size: 0.91rem;
            line-height: 1.55;
          }
          .eyebrow-note {
            color: #8679cc;
            font-size: 0.68rem;
            font-weight: 720;
            letter-spacing: 0.12em;
          }
          .empty-state {
            padding: 2rem 1.2rem;
            border: 1px dashed #d8dceb;
            border-radius: 0.95rem;
            background: rgba(255, 255, 255, 0.72);
            text-align: center;
          }
          .empty-state h3 {
            margin: 0.15rem 0 0.4rem;
            color: #26314f;
            font-size: 1.08rem;
            font-weight: 680;
          }
          .empty-state p {
            max-width: 32rem;
            margin: 0 auto;
            color: #768098;
            font-size: 0.89rem;
            line-height: 1.55;
          }
          .document-name {
            overflow-wrap: anywhere;
            color: #26314f;
            font-size: 0.98rem;
            font-weight: 670;
          }
          .feature-label {
            color: #8174cb;
            font-size: 0.68rem;
            font-weight: 730;
            letter-spacing: 0.1em;
          }
          div[data-testid="stMetric"] {
            padding: 0.1rem 0;
          }
          div[data-testid="stMetricLabel"] {
            color: #798198;
            font-size: 0.78rem;
          }
          div[data-testid="stMetricValue"] {
            color: #202b49;
            font-size: 1.85rem;
            font-weight: 700;
            letter-spacing: -0.05em;
          }
          div[data-testid="stVerticalBlockBorderWrapper"] {
            border-color: var(--line);
            border-radius: 0.95rem;
            background: var(--surface);
          }
          .stButton > button {
            border-radius: 0.68rem;
            font-weight: 620;
            transition: transform 120ms ease, box-shadow 120ms ease;
          }
          .stButton > button:hover:not(:disabled) {
            transform: translateY(-1px);
            box-shadow: 0 5px 14px rgba(38, 42, 82, 0.08);
          }
          .stTextArea textarea, .stTextInput input {
            border-radius: 0.7rem;
          }
          @media (max-width: 760px) {
            [data-testid="stAppViewContainer"] > .main .block-container {
              padding: 1.35rem 1.1rem 3rem;
            }
            .page-heading { flex-direction: column; margin-bottom: 1.5rem; }
            .connection-badge { margin-top: 0; }
          }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_page_header(*, title: str, subtitle: str, eyebrow: str) -> None:
    """Render the page heading with the configured AI status."""
    if groq_is_configured():
        status_text = "Groq AI connected"
        status_color = "#22c55e"
    else:
        status_text = "Local AI mode"
        status_color = "#f59e0b"

    st.markdown(
        f"""
        <div class="page-heading">
          <div>
            <p class="page-eyebrow">{escape(eyebrow)}</p>
            <h1 class="page-title">{escape(title)}</h1>
            <p class="page-subtitle">{escape(subtitle)}</p>
          </div>
          <div class="connection-badge">
            <span
              class="badge-dot"
              style="background-color: {status_color};"
            ></span>
            {escape(status_text)}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def navigate_to(page: str) -> None:
    """Navigate from a page action using Streamlit's callback phase."""
    if page in PAGE_DETAILS:
        st.session_state["active_page"] = page


def render_empty_state(title: str, message: str) -> None:
    st.markdown(
        f"""
        <div class="empty-state">
          <h3>{escape(title)}</h3>
          <p>{escape(message)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def format_bytes(size: int) -> str:
    if size < 1024:
        return f"{size} B"
    if size < 1024 * 1024:
        return f"{size / 1024:.0f} KB"
    return f"{size / (1024 * 1024):.1f} MB"
