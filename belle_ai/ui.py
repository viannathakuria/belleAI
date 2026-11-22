
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
    try:
        return bool(st.secrets.get("GROQ_API_KEY"))
    except Exception:
        return False


def inject_styles() -> None:
    """Apply belleAI's accessible pink-and-blue theme."""

    st.markdown(
        """
<style>

/* ==========================================
   BELLEAI — PINK + BLUE DESIGN SYSTEM
   ========================================== */

:root {
    --belle-ink: #243657;
    --belle-heading: #1d3054;
    --belle-muted: #526583;

    --belle-pink: #c34e8c;
    --belle-pink-dark: #923462;
    --belle-pink-light: #f9dce9;

    --belle-blue: #4789c5;
    --belle-blue-dark: #27679e;
    --belle-blue-light: #e8f4ff;

    --belle-background: #fff7fb;
    --belle-white: #ffffff;
    --belle-border: #e7cbdc;

    --belle-gradient:
        linear-gradient(110deg, #c34e8c, #4789c5);
}

/* ==========================================
   MAIN APPLICATION
   ========================================== */

.stApp {
    background: var(--belle-background);
    color: var(--belle-ink);
    font-family:
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: var(--belle-background);
}

[data-testid="stHeader"] {
    background: rgba(255, 247, 251, 0.96);
}

[data-testid="stAppViewContainer"]
> .main .block-container {
    max-width: 1480px;
    padding: 2rem 3rem 4rem;
}

/* Default content text */

[data-testid="stMain"] p,
[data-testid="stMain"] li,
[data-testid="stMain"] label {
    color: var(--belle-ink);
}

[data-testid="stMain"] h1,
[data-testid="stMain"] h2,
[data-testid="stMain"] h3,
[data-testid="stMain"] h4 {
    color: var(--belle-heading);
}

[data-testid="stMain"] a {
    color: var(--belle-blue-dark);
}

/* ==========================================
   SIDEBAR
   ========================================== */

[data-testid="stSidebar"] {
    background: #fff1f7;
    border-right: 1px solid var(--belle-border);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.6rem;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label {
    color: var(--belle-ink);
}

/* Branding */

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
    background: var(--belle-gradient);
    color: #ffffff;
    font-size: 1.55rem;
    font-weight: 700;
    line-height: 1;
}

.brand-name {
    color: var(--belle-heading);
    font-size: 1.17rem;
    font-weight: 720;
    letter-spacing: -0.045em;
}

.brand-name span {
    color: var(--belle-pink-dark);
}

.brand-caption {
    margin-top: 0.16rem;
    color: var(--belle-muted);
    font-size: 0.58rem;
    font-weight: 700;
    letter-spacing: 0.14em;
}

.sidebar-section-label {
    margin: 0.5rem 0 0.45rem 0.45rem;
    color: #77536b;
    font-size: 0.67rem;
    font-weight: 750;
    letter-spacing: 0.13em;
}

/* Sidebar navigation */

[data-testid="stSidebar"] [role="radiogroup"] {
    gap: 0.22rem;
}

[data-testid="stSidebar"]
[role="radiogroup"] label {
    min-height: 2.65rem;
    padding: 0.45rem 0.65rem;
    border-radius: 0.7rem;
    color: #344765;
    font-size: 0.9rem;
    transition: background 140ms ease;
}

[data-testid="stSidebar"]
[role="radiogroup"] label:has(input:checked) {
    background: #f7d8e7;
    color: #7c2855;
    font-weight: 700;
}

[data-testid="stSidebar"]
[role="radiogroup"] label:has(input:checked) p {
    color: #7c2855 !important;
}

[data-testid="stSidebar"]
[role="radiogroup"] label > div:first-child {
    display: none;
}

/* Sidebar connection status */

.sidebar-status {
    margin: 0.5rem 0 0.35rem;
    padding: 0.9rem 0.85rem;
    border: 1px solid #e7bcd0;
    border-radius: 0.8rem;
    background: #ffffff;
}

.sidebar-status-title {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    color: var(--belle-heading);
    font-size: 0.79rem;
    font-weight: 700;
}

.status-dot {
    width: 0.45rem;
    height: 0.45rem;
    border-radius: 50%;
    background: #b9bfd0;
}

.sidebar-status-copy {
    margin: 0.35rem 0 0 0.9rem;
    color: var(--belle-muted);
    font-size: 0.75rem;
}

/* ==========================================
   PAGE HEADINGS
   ========================================== */

.page-heading {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 1rem;
    margin: 0.1rem 0 2rem;
}

.page-eyebrow {
    margin: 0 0 0.45rem;
    color: #a33b73;
    font-size: 0.7rem;
    font-weight: 800;
    letter-spacing: 0.14em;
}

.page-title {
    margin: 0;
    color: var(--belle-heading);
    font-size: clamp(1.7rem, 3vw, 2.35rem);
    font-weight: 750;
    letter-spacing: -0.055em;
    line-height: 1.14;
}

.page-subtitle {
    margin: 0.62rem 0 0;
    color: var(--belle-muted);
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
    border: 1px solid #e7bfd2;
    border-radius: 999px;
    background: #ffffff;
    color: var(--belle-heading);
    font-size: 0.76rem;
    font-weight: 700;
}

.badge-dot {
    width: 0.42rem;
    height: 0.42rem;
    border-radius: 50%;
    background: #c1c5d0;
}

.section-intro {
    margin: -0.75rem 0 1.35rem;
    color: var(--belle-muted);
    font-size: 0.91rem;
    line-height: 1.55;
}

.eyebrow-note {
    color: var(--belle-pink-dark);
    font-size: 0.7rem;
    font-weight: 750;
    letter-spacing: 0.12em;
}

/* ==========================================
   DASHBOARD CARDS
   ========================================== */

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: #e5c3d6;
    border-radius: 0.95rem;
    background: #ffffff;
}

/* METRIC LABEL FIX */

[data-testid="stMetric"] {
    padding: 0.1rem 0;
    color: var(--belle-heading) !important;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] *,
[data-testid="stMetricLabel"] p,
[data-testid="stMetricLabel"] span {
    color: #344765 !important;
    -webkit-text-fill-color: #344765 !important;
    opacity: 1 !important;
    font-size: 0.95rem !important;
    font-weight: 750 !important;
}

[data-testid="stMetricValue"],
[data-testid="stMetricValue"] *,
[data-testid="stMetricValue"] p {
    color: #203455 !important;
    -webkit-text-fill-color: #203455 !important;
    opacity: 1 !important;
    font-weight: 800 !important;
}

[data-testid="stMetricDelta"],
[data-testid="stMetricDelta"] * {
    font-weight: 650;
    opacity: 1 !important;
}

/* ==========================================
   EMPTY STATES AND DOCUMENTS
   ========================================== */

.empty-state {
    padding: 2rem 1.2rem;
    border: 1px dashed #e4a8c4;
    border-radius: 0.95rem;
    background: #ffffff;
    text-align: center;
}

.empty-state h3 {
    margin: 0.15rem 0 0.4rem;
    color: var(--belle-heading);
    font-size: 1.08rem;
    font-weight: 750;
}

.empty-state p {
    max-width: 32rem;
    margin: 0 auto;
    color: var(--belle-muted);
    font-size: 0.89rem;
    line-height: 1.55;
}

.document-name {
    overflow-wrap: anywhere;
    color: var(--belle-heading);
    font-size: 0.98rem;
    font-weight: 700;
}

.feature-label {
    color: var(--belle-pink-dark);
    font-size: 0.7rem;
    font-weight: 750;
    letter-spacing: 0.1em;
}

/* ==========================================
   BUTTONS
   ========================================== */

.stButton > button,
.stDownloadButton > button {
    border-radius: 0.7rem !important;
    font-weight: 700 !important;
    transition:
        background 140ms ease,
        box-shadow 140ms ease;
}

/* Secondary buttons */

.stButton > button:not([kind="primary"]),
.stDownloadButton > button:not([kind="primary"]) {
    background: #ffffff !important;
    color: #81335e !important;
    border: 1px solid #dc9ebc !important;
}

.stButton > button:not([kind="primary"]) *,
.stDownloadButton > button:not([kind="primary"]) * {
    color: #81335e !important;
}

.stButton > button:not([kind="primary"]):hover,
.stDownloadButton > button:not([kind="primary"]):hover {
    background: #fce5ef !important;
    border-color: #bf6092 !important;
}

/* Primary buttons */

.stButton > button[kind="primary"],
.stDownloadButton > button[kind="primary"] {
    background: var(--belle-gradient) !important;
    color: #ffffff !important;
    border: 1px solid transparent !important;
}

.stButton > button[kind="primary"] *,
.stDownloadButton > button[kind="primary"] * {
    color: #ffffff !important;
}

.stButton > button:disabled,
.stDownloadButton > button:disabled {
    opacity: 0.65;
    cursor: not-allowed;
}

/* ==========================================
   TEXT INPUTS AND TEXT AREAS
   ========================================== */

[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
.stTextInput input,
.stTextArea textarea {
    background: #ffffff !important;
    color: #203455 !important;
    border-radius: 0.7rem !important;
    caret-color: #a43d78 !important;
}

[data-testid="stTextInput"] input::placeholder,
[data-testid="stTextArea"] textarea::placeholder {
    color: #66738b !important;
    opacity: 1 !important;
}

[data-testid="stTextInput"] label,
[data-testid="stTextArea"] label {
    color: #293d5f !important;
    font-weight: 650 !important;
}

/* ==========================================
   CHAT MESSAGES
   ========================================== */

[data-testid="stChatMessage"] {
    background: #e8f4ff !important;
    border: 1px solid #a9cde9 !important;
    border-radius: 1rem !important;
    padding: 1.15rem 1.3rem !important;
    margin-bottom: 1rem !important;
    box-shadow: 0 2px 8px rgba(35, 54, 92, 0.05);
}

/* User messages: pink */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) {
    background: #f9dce9 !important;
    border: 1px solid #e4aac5 !important;
}

/* AI messages: blue */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) {
    background: #e8f4ff !important;
    border: 1px solid #a9cde9 !important;
    border-left: 4px solid #4789c5 !important;
}

/* Chat text */

[data-testid="stChatMessage"]
[data-testid="stMarkdownContainer"],
[data-testid="stChatMessage"]
[data-testid="stMarkdownContainer"] p,
[data-testid="stChatMessage"]
[data-testid="stMarkdownContainer"] li {
    color: #203455 !important;
    font-size: 1rem !important;
    line-height: 1.75 !important;
}

[data-testid="stChatMessage"]
[data-testid="stMarkdownContainer"] strong {
    color: #142849 !important;
    font-weight: 800 !important;
}

[data-testid="stChatMessage"]
[data-testid="stMarkdownContainer"] a {
    color: #923462 !important;
    text-decoration: underline;
}

[data-testid="stChatMessage"]
[data-testid="stMarkdownContainer"] code {
    color: #203455 !important;
    background: #ffffff !important;
}

[data-testid="stChatMessage"]
[data-testid="stMarkdownContainer"] hr {
    border-color: #b6cce2 !important;
}

[data-testid="stChatMessage"]
[data-testid="stCaptionContainer"],
[data-testid="stChatMessage"] small {
    color: #435775 !important;
}

/* ==========================================
   CHAT INPUT
   ========================================== */

/* Fix outer input and inner white rectangle */

[data-testid="stChatInput"] {
    background: #fff0f7 !important;
    border: 1.5px solid #d99ebc !important;
    border-radius: 14px !important;
    box-shadow: 0 3px 12px rgba(195, 78, 140, 0.08) !important;
}

[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] > div > div,
[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] textarea:focus,
[data-testid="stChatInput"] [data-baseweb],
[data-testid="stChatInput"] [data-baseweb] > div {
    background: transparent !important;
    background-color: transparent !important;
    color: #203455 !important;
    box-shadow: none !important;
}

[data-testid="stChatInput"] textarea {
    color: #203455 !important;
    -webkit-text-fill-color: #203455 !important;
    caret-color: #a43d78 !important;
    font-size: 1rem !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #655f77 !important;
    -webkit-text-fill-color: #655f77 !important;
    opacity: 1 !important;
}

[data-testid="stChatInput"] button {
    background: #c34e8c !important;
    color: #ffffff !important;
    border-radius: 10px !important;
}

[data-testid="stChatInput"] button svg {
    color: #ffffff !important;
    stroke: #ffffff !important;
}

/* Bottom composer area */

[data-testid="stBottom"] {
    background: #fff7fb !important;
}

[data-testid="stBottomBlockContainer"] {
    background: #fff7fb !important;
}

/* ==========================================
   ALERTS AND NOTIFICATIONS
   ========================================== */

/* Information */

[data-testid="stAlert"][data-baseweb="notification"] {
    border-radius: 0.8rem;
}

[data-testid="stAlert"] {
    color: #203455 !important;
}

[data-testid="stAlert"] p,
[data-testid="stAlert"] li,
[data-testid="stAlert"] span {
    color: #203455 !important;
    opacity: 1 !important;
}

[data-testid="stAlert"] a {
    color: #245c91 !important;
}

/* Info alerts */

[data-testid="stAlert"]:has(
    [data-testid="stNotificationContentInfo"]
) {
    background: #e8f4ff !important;
    border: 1px solid #a9cde9 !important;
}

/* Success alerts */

[data-testid="stAlert"]:has(
    [data-testid="stNotificationContentSuccess"]
) {
    background: #eaf8f1 !important;
    border: 1px solid #9ed4b7 !important;
}

/* Warning alerts */

[data-testid="stAlert"]:has(
    [data-testid="stNotificationContentWarning"]
) {
    background: #fff2df !important;
    border: 1px solid #e5c18a !important;
}

/* Error alerts */

[data-testid="stAlert"]:has(
    [data-testid="stNotificationContentError"]
) {
    background: #fff0f2 !important;
    border: 1px solid #e8a7b4 !important;
}

/* ==========================================
   FILE UPLOADER
   ========================================== */

[data-testid="stFileUploader"] {
    color: var(--belle-ink);
}

[data-testid="stFileUploaderDropzone"] {
    background: #fffafd !important;
    border: 2px dashed #dba9c5 !important;
    border-radius: 0.9rem !important;
}

[data-testid="stFileUploaderDropzone"] *,
[data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] small {
    color: #344765 !important;
}

[data-testid="stFileUploaderDropzone"] button {
    background: #ffffff !important;
    color: #81335e !important;
    border: 1px solid #dba9c5 !important;
    border-radius: 0.65rem !important;
}

/* ==========================================
   SELECT BOXES AND DROPDOWNS
   ========================================== */

[data-testid="stSelectbox"] label,
[data-testid="stMultiSelect"] label {
    color: #293d5f !important;
    font-weight: 650 !important;
}

[data-testid="stSelectbox"] [data-baseweb="select"],
[data-testid="stMultiSelect"] [data-baseweb="select"] {
    background: #ffffff !important;
    color: #203455 !important;
}

[data-testid="stSelectbox"] [data-baseweb="select"] > div,
[data-testid="stMultiSelect"] [data-baseweb="select"] > div {
    background: #ffffff !important;
    color: #203455 !important;
    border-color: #dba9c5 !important;
}

[data-baseweb="popover"],
[data-baseweb="menu"],
[data-baseweb="list"] {
    background: #ffffff !important;
    color: #203455 !important;
}

[data-baseweb="menu"] li,
[data-baseweb="menu"] [role="option"] {
    color: #203455 !important;
}

/* ==========================================
   CHECKBOXES, TOGGLES AND RADIO BUTTONS
   ========================================== */

[data-testid="stCheckbox"] label,
[data-testid="stToggle"] label,
[data-testid="stRadio"] label {
    color: #293d5f !important;
}

[data-testid="stCheckbox"] p,
[data-testid="stToggle"] p,
[data-testid="stRadio"] p {
    color: #293d5f !important;
}

/* ==========================================
   TABS
   ========================================== */

[data-baseweb="tab-list"] {
    border-bottom-color: #e8bfd3 !important;
}

[data-baseweb="tab"] {
    color: #526583 !important;
    font-weight: 650 !important;
}

[data-baseweb="tab"][aria-selected="true"] {
    color: #923462 !important;
    font-weight: 750 !important;
}

/* ==========================================
   EXPANDERS
   ========================================== */

[data-testid="stExpander"] {
    background: #ffffff;
    border: 1px solid #e7cbdc;
    border-radius: 0.8rem;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary * {
    color: #263b5e !important;
}

/* ==========================================
   DATAFRAMES AND TABLES
   ========================================== */

[data-testid="stTable"] {
    color: #203455;
}

[data-testid="stTable"] th {
    background: #f9dce9 !important;
    color: #203455 !important;
}

[data-testid="stTable"] td {
    color: #203455 !important;
}

/* ==========================================
   CAPTIONS AND DIVIDERS
   ========================================== */

[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p {
    color: #526583 !important;
    opacity: 1 !important;
}

hr {
    border-color: #e7cbdc !important;
}

/* ==========================================
   MOBILE RESPONSIVENESS
   ========================================== */

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

    .page-title {
        font-size: 1.8rem;
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] * {
        font-size: 0.85rem !important;
    }
}

</style>
        """,
        unsafe_allow_html=True,
    )


def render_page_header(
    *,
    title: str,
    subtitle: str,
    eyebrow: str,
) -> None:
    """Render the page heading and AI connection indicator."""

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
    """Navigate to a page using Streamlit session state."""

    if page in PAGE_DETAILS:
        st.session_state["active_page"] = page


def render_empty_state(
    title: str,
    message: str,
) -> None:
    """Display a readable empty-state card."""

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
    """Format file sizes for display."""

    if size < 1024:
        return f"{size} B"

    if size < 1024 * 1024:
        return f"{size / 1024:.0f} KB"

    return f"{size / (1024 * 1024):.1f} MB"
