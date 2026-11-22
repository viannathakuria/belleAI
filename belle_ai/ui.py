
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
    """Apply belleAI's pink and blue theme."""
    st.markdown(
        """
        <style>
          :root {
            --ink: #26365c;
            --muted: #596987;
            --line: #ecdce8;
            --lavender: #c65391;
            --lavender-soft: #fff0f7;
            --surface: #ffffff;
            --pink: #f9d7e6;
            --blue: #eaf5ff;
          }

          .stApp {
            background: #fff7fa;
            color: var(--ink);
            font-family: Inter, ui-sans-serif, system-ui,
              -apple-system, BlinkMacSystemFont, "Segoe UI",
              sans-serif;
          }

          [data-testid="stHeader"] {
            background: rgba(255, 247, 250, 0.95);
          }

          [data-testid="stAppViewContainer"] > .main .block-container {
            max-width: 1480px;
            padding: 2rem 3rem 4rem;
          }

          [data-testid="stSidebar"] {
            background: #fff;
            border-right: 1px solid #f0dce8;
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
            background: linear-gradient(
              135deg, #df6fa8, #78b9ef
            );
            color: #fff;
            font-size: 1.55rem;
            font-weight: 700;
            line-height: 1;
          }

          .brand-name {
            color: #26365c;
            font-size: 1.17rem;
            font-weight: 720;
            letter-spacing: -0.045em;
          }

          .brand-name span {
            color: #c65391;
          }

          .brand-caption {
            margin-top: 0.16rem;
            color: #697995;
            font-size: 0.58rem;
            font-weight: 700;
            letter-spacing: 0.14em;
          }

          .sidebar-section-label {
            margin: 0.5rem 0 0.45rem 0.45rem;
            color: #697995;
            font-size: 0.64rem;
            font-weight: 700;
            letter-spacing: 0.13em;
          }

          [data-testid="stSidebar"] [role="radiogroup"] {
            gap: 0.22rem;
          }

          [data-testid="stSidebar"] [role="radiogroup"] label {
            min-height: 2.65rem;
            padding: 0.45rem 0.65rem;
            border-radius: 0.7rem;
            color: #455676;
            font-size: 0.9rem;
            transition: background 140ms ease,
                        color 140ms ease;
          }

          [data-testid="stSidebar"] [role="radiogroup"]
          label:has(input:checked) {
            background: #ffe4f0;
            color: #91366c;
            font-weight: 650;
          }

          [data-testid="stSidebar"] [role="radiogroup"]
          label > div:first-child {
            display: none;
          }

          .sidebar-status {
            margin: 0.5rem 0 0.35rem;
            padding: 0.9rem 0.85rem;
            border: 1px solid #f0dce8;
            border-radius: 0.8rem;
            background: #fff9fc;
          }

          .sidebar-status-title {
            display: flex;
            align-items: center;
            gap: 0.45rem;
            color: #26365c;
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
            color: #586987;
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
            color: #b24784;
            font-size: 0.67rem;
            font-weight: 750;
            letter-spacing: 0.14em;
          }

          .page-title {
            margin: 0;
            color: #26365c;
            font-size: clamp(1.7rem, 3vw, 2.35rem);
            font-weight: 720;
            letter-spacing: -0.055em;
            line-height: 1.14;
          }

          .page-subtitle {
            margin: 0.62rem 0 0;
            color: #596987;
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
            border: 1px solid #f0dce8;
            border-radius: 999px;
            background: #ffffff;
            color: #455676;
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
            color: #596987;
            font-size: 0.91rem;
            line-height: 1.55;
          }

          .eyebrow-note {
            color: #b24784;
            font-size: 0.68rem;
            font-weight: 720;
            letter-spacing: 0.12em;
          }

          .empty-state {
            padding: 2rem 1.2rem;
            border: 1px dashed #eabfd5;
            border-radius: 0.95rem;
            background: #ffffff;
            text-align: center;
          }

          .empty-state h3 {
            margin: 0.15rem 0 0.4rem;
            color: #26365c;
            font-size: 1.08rem;
            font-weight: 680;
          }

          .empty-state p {
            max-width: 32rem;
            margin: 0 auto;
            color: #596987;
            font-size: 0.89rem;
            line-height: 1.55;
          }

          .document-name {
            overflow-wrap: anywhere;
            color: #26365c;
            font-size: 0.98rem;
            font-weight: 670;
          }

          .feature-label {
            color: #b24784;
            font-size: 0.68rem;
            font-weight: 730;
            letter-spacing: 0.1em;
          }

          div[data-testid="stMetric"] {
            padding: 0.1rem 0;
          }

          div[data-testid="stMetricLabel"] {
            color: #596987;
            font-size: 0.78rem;
          }

          div[data-testid="stMetricValue"] {
            color: #26365c;
            font-size: 1.85rem;
            font-weight: 700;
            letter-spacing: -0.05em;
          }

          div[data-testid="stVerticalBlockBorderWrapper"] {
            border-color: #f0dce8;
            border-radius: 0.95rem;
            background: #ffffff;
          }

          .stButton > button {
            border-radius: 0.68rem;
            font-weight: 620;
            transition: transform 120ms ease,
                        box-shadow 120ms ease;
          }

          .stButton > button:hover:not(:disabled) {
            transform: translateY(-1px);
            box-shadow: 0 5px 14px
              rgba(130, 63, 112, 0.12);
          }

          .stTextArea textarea,
          .stTextInput input {
            border-radius: 0.7rem;
          }

          /* Pink user messages */

          [data-testid="stChatMessage"] {
            background: #eaf5ff !important;
            border: 1px solid #b9dfff !important;
            border-radius: 1rem !important;
            padding: 1.15rem 1.3rem !important;
            margin-bottom: 1rem !important;
            box-shadow: 0 2px 8px
              rgba(35, 54, 92, 0.05);
          }

          [data-testid="stChatMessage"]:has(
            [data-testid="chatAvatarIcon-user"]
          ) {
            background: #f9d7e6 !important;
            border-color: #e8a9c9 !important;
          }

          /* Blue AI messages */

          [data-testid="stChatMessage"]:has(
            [data-testid="chatAvatarIcon-assistant"]
          ) {
            background: #eaf5ff !important;
            border-left: 4px solid #6aa8de !important;
          }

          [data-testid="stChatMessage"]
          [data-testid="stMarkdownContainer"],
          [data-testid="stChatMessage"]
          [data-testid="stMarkdownContainer"] p,
          [data-testid="stChatMessage"]
          [data-testid="stMarkdownContainer"] li {
            color: #26365c !important;
            font-size: 1rem !important;
            line-height: 1.75 !important;
          }

          [data-testid="stChatMessage"]
          [data-testid="stMarkdownContainer"] strong {
            color: #172744 !important;
            font-weight: 750 !important;
          }

          [data-testid="stChatMessage"]
          [data-testid="stMarkdownContainer"] a {
            color: #91416f !important;
            text-decoration: underline;
          }

          [data-testid="stChatMessage"]
          [data-testid="stMarkdownContainer"] code {
            color: #26365c !important;
            background: #ffffff !important;
          }

          [data-testid="stChatMessage"]
          [data-testid="stCaptionContainer"],
          [data-testid="stChatMessage"] small {
            color: #455676 !important;
          }

          /* Pink chat composer */

          [data-testid="stChatInput"],
          [data-testid="stBottom"]
          [data-testid="stChatInput"] {
            background: #fff0f7 !important;
            border: 1.5px solid #eab6d0 !important;
            border-radius: 14px !important;
            box-shadow: 0 3px 12px
              rgba(198, 83, 145, 0.08) !important;
          }

          [data-testid="stChatInput"] > div,
          [data-testid="stChatInput"] textarea,
          [data-testid="stChatInput"] textarea:focus,
          [data-testid="stChatInput"] [data-baseweb],
          [data-testid="stChatInput"] [data-baseweb] > div {
            background: transparent !important;
            background-color: transparent !important;
            color: #26365c !important;
            box-shadow: none !important;
          }

          [data-testid="stChatInput"] textarea::placeholder {
            color: #71677d !important;
            opacity: 1 !important;
          }

          [data-testid="stChatInput"] button {
            background: #c65391 !important;
            color: #ffffff !important;
            border-radius: 10px !important;
          }

          [data-testid="stChatInput"] button svg {
            color: #ffffff !important;
          }

          /* Readable buttons */

          .stButton > button:not([kind="primary"]) {
            background: #ffffff;
            color: #833660;
            border: 1px solid #eab6d0;
          }

          .stButton > button:not([kind="primary"]):hover {
            background: #ffe8f2;
            color: #833660;
          }

          .stButton > button[kind="primary"] {
            background: linear-gradient(
              110deg, #c65391, #518ac6
            );
            color: #ffffff;
            border: none;
          }

          /* Mobile */

          @media (max-width: 760px) {
            [data-testid="stAppViewContainer"]
            > .main .block-container {
              padding: 1.35rem 1.1rem 3rem;
            }

            .page-heading {
              flex-direction: column;
              margin-bottom: 1.5rem;
            }

            .connection-badge {
              margin-top: 0;
            }

            [data-testid="stChatMessage"] {
              padding: 0.85rem 0.8rem !important;
            }
          }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_page_header(
    *, title: str, subtitle: str, eyebrow: str
) -> None:
    """Render the page heading with configured AI status."""
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
    """Navigate from a page action."""
    if page in PAGE_DETAILS:
        st.session_state["active_page"] = page


def render_empty_state(
    title: str, message: str
) -> None:
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
