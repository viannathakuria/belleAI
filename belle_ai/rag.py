
"""Hybrid PDF retrieval: keyword + semantic embeddings + reciprocal rank fusion."""
from __future__ import annotations

import hashlib
import re
from collections import Counter

import numpy as np
import streamlit as st
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
PAGE_PATTERN = re.compile(r"--- Page (\d+) ---\s*")
WORD_PATTERN = re.compile(r"[a-z0-9]{2,}")
STOP_WORDS = set("the and for what how does this that with from about please explain tell which are was were have has had you your can could would should into onto there their they them then than when where why who what did not but also using use pdf document page find give show me of to in on at by is it a an as or be do i".split())


@st.cache_resource(show_spinner="Loading semantic search model (first use may take a minute)...")
def get_embedding_model():
    return SentenceTransformer(MODEL_NAME)


def tokenize(text: str):
    return [word for word in WORD_PATTERN.findall(text.lower()) if word not in STOP_WORDS]


def chunk_document(text: str, name: str, chunk_size: int = 1100, overlap: int = 180):
    """Split pages into overlapping passages and retain exact PDF page metadata."""
    chunks = []
    parts = PAGE_PATTERN.split(text)
    for i in range(1, len(parts), 2):
        page = int(parts[i])
        page_text = re.sub(r"\s+", " ", parts[i + 1]).strip()
        start = 0
        while start < len(page_text):
            end = min(start + chunk_size, len(page_text))
            if end < len(page_text):
                boundary = page_text.rfind(" ", start + chunk_size // 2, end)
                if boundary > start:
                    end = boundary
            piece = page_text[start:end].strip()
            if piece:
                chunks.append({"name": name, "page": page, "text": piece})
            if end >= len(page_text):
                break
            start = max(start + 1, end - overlap)
    return chunks


def get_relevant_pages(question: str, documents: dict, max_pages: int = 5):
    """Fuse keyword BM25-style rankings and semantic cosine rankings via RRF."""
    fingerprints = tuple(sorted(
        (str(doc_id), hashlib.sha256(doc.get("text", "").encode(
            "utf-8")).hexdigest(), doc.get("name", ""))
        for doc_id, doc in documents.items() if doc.get("text")
    ))
    if not fingerprints:
        return []

    cache = st.session_state.get("belleai_hybrid_index")
    if cache is None or cache["fingerprints"] != fingerprints:
        chunks = []
        for doc_id in sorted(documents, key=str):
            doc = documents[doc_id]
            if doc.get("text"):
                chunks.extend(chunk_document(
                    doc["text"], doc.get("name", "Document.pdf")))
        if not chunks:
            return []
        model = get_embedding_model()
        vectors = model.encode(
            [chunk["text"] for chunk in chunks],
            batch_size=32, convert_to_numpy=True,
            normalize_embeddings=True, show_progress_bar=False,
        )
        token_counts = [Counter(tokenize(chunk["text"])) for chunk in chunks]
        lengths = np.array([sum(counts.values())
                           for counts in token_counts], dtype=float)
        doc_freq = Counter()
        for counts in token_counts:
            doc_freq.update(counts.keys())
        cache = {
            "fingerprints": fingerprints, "chunks": chunks, "vectors": vectors,
            "token_counts": token_counts, "lengths": lengths,
            "doc_freq": doc_freq,
        }
        st.session_state["belleai_hybrid_index"] = cache

    model = get_embedding_model()
    query_vector = model.encode(
        [question], convert_to_numpy=True,
        normalize_embeddings=True, show_progress_bar=False,
    )[0]
    semantic_scores = np.asarray(cache["vectors"] @ query_vector)
    semantic_order = np.argsort(-semantic_scores, kind="stable")

    # BM25 keyword scoring, useful for exact terms, names, and acronyms.
    query_terms = set(tokenize(question))
    n = len(cache["chunks"])
    avg_len = max(float(np.mean(cache["lengths"])), 1.0)
    keyword_scores = np.zeros(n, dtype=float)
    for term in query_terms:
        df = cache["doc_freq"].get(term, 0)
        idf = np.log(1.0 + (n - df + 0.5) / (df + 0.5))
        for i, counts in enumerate(cache["token_counts"]):
            tf = counts.get(term, 0)
            if tf:
                norm = 1.2 * (0.25 + 0.75 * cache["lengths"][i] / avg_len)
                keyword_scores[i] += idf * (tf * 2.2) / (tf + norm)

    keyword_order = np.argsort(-keyword_scores, kind="stable")
    # Only contribute keyword ranks with actual lexical matches.
    fused = np.zeros(n, dtype=float)
    for rank, index in enumerate(semantic_order):
        fused[index] += 1.0 / (60 + rank + 1)
    for rank, index in enumerate(keyword_order):
        if keyword_scores[index] <= 0:
            break
        fused[index] += 1.0 / (60 + rank + 1)

    best = np.argsort(-fused, kind="stable")[:max_pages]
    return [
        {**cache["chunks"][int(i)], "score": float(fused[int(i)])}
        for i in best
    ]
