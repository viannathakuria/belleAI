# belleAI

belleAI is a Streamlit research workspace for collecting PDF papers and reading
their extracted text. This first phase includes a working document library and
clearly labeled previews for features that are not connected yet.

## What works now

- Upload one or more PDF files and extract selectable text with PyMuPDF.
- Review document names, page counts, file sizes, and extracted text.
- Remove documents from the current session.
- Navigate between the dashboard, document library, research chat, image
  analysis, knowledge graph, and settings.
- Preview an image locally on the Image Analysis page.

The research chat does not generate answers yet. Gemini is not connected, and
the image analysis and knowledge graph pages are previews only. No AI output is
fabricated.

## Run locally

Requires Python 3.10 or newer.

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit (usually `http://localhost:8501`).

## Privacy and storage

PDF contents are kept in the Streamlit app's in-memory session state while the
session is active. belleAI does not write uploaded documents to disk, send them
to an AI service, or persist them between sessions in this phase. Documents
with no selectable text (for example, scanned pages) can be added, but OCR is
not included.

## Project structure

```text
app.py                         Streamlit entry point and page navigation
belle_ai/
  document_processing.py       PDF validation and text extraction
  ui.py                        Shared page headers, navigation, and styling
  pages/
    dashboard.py               Workspace overview
    documents.py               Upload, review, and removal
    research_chat.py           Explicitly inactive chat preview
    feature_previews.py        Image analysis and knowledge graph previews
    settings.py                Session and integration status
requirements.txt               Python dependencies
```

Gemini, FAISS, and NetworkX are intentionally not included in this first phase.
