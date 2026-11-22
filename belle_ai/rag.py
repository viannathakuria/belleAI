
"""
belleAI Hybrid RAG

Features:
- PDF text chunking
- Query normalization
- BM25 keyword retrieval
- Semantic embedding retrieval
- Reciprocal Rank Fusion (RRF)
- Source diversity to reduce duplicate page references
- Session-level embedding caching
"""

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

STOP_WORDS = set(
    """
    the and for what how does this that with from about
    please explain tell which are was were have has had
    you your can could would should into onto there
    their they them then than when where why who did
    not but also using use pdf document page find give
    show me of to in on at by is it a an as or be do i
    """.split()
)


@st.cache_resource(
    show_spinner="Loading semantic search model..."
)
def get_embedding_model():
    """Load the embedding model once per Streamlit process."""
    return SentenceTransformer(MODEL_NAME)


def normalize_text(text: str) -> str:
    """
    Normalize variations in topic and section numbering.

    Examples:
        topic1    -> topic 1
        topic-1   -> topic 1
        Topic_1   -> topic 1
        topic 1   -> topic 1
        section2  -> section 2
    """
    text = text.lower().strip()

    # Separate letters and numbers.
    text = re.sub(r"([a-z])(\d)", r"\1 \2", text)
    text = re.sub(r"(\d)([a-z])", r"\1 \2", text)

    # Treat common separators consistently.
    text = re.sub(r"(?<=[a-z])[-_](?=\d)", " ", text)

    # Collapse repeated whitespace.
    text = re.sub(r"\s+", " ", text)

    return text


def tokenize(text: str) -> list[str]:
    """Tokenize normalized text for keyword retrieval."""
    normalized = normalize_text(text)

    return [
        word
        for word in WORD_PATTERN.findall(normalized)
        if word not in STOP_WORDS
    ]


def chunk_document(
    text: str,
    name: str,
    chunk_size: int = 1100,
    overlap: int = 180,
) -> list[dict]:
    """
    Split each PDF page into overlapping chunks.

    Every chunk retains its original document name
    and page number for citations.
    """
    chunks = []

    parts = PAGE_PATTERN.split(text)

    for i in range(1, len(parts), 2):
        page_number = int(parts[i])

        page_text = re.sub(
            r"\s+",
            " ",
            parts[i + 1],
        ).strip()

        if not page_text:
            continue

        start = 0

        while start < len(page_text):
            end = min(
                start + chunk_size,
                len(page_text),
            )

            # Prefer ending chunks at word boundaries.
            if end < len(page_text):
                boundary = page_text.rfind(
                    " ",
                    start + chunk_size // 2,
                    end,
                )

                if boundary > start:
                    end = boundary

            chunk_text = page_text[start:end].strip()

            if chunk_text:
                chunks.append(
                    {
                        "name": name,
                        "page": page_number,
                        "text": chunk_text,
                    }
                )

            if end >= len(page_text):
                break

            start = max(
                start + 1,
                end - overlap,
            )

    return chunks


def build_index(documents: dict) -> dict | None:
    """
    Build or reuse the document retrieval index.

    Embeddings are cached in Streamlit session state.
    """
    fingerprints = tuple(
        sorted(
            (
                str(doc_id),
                hashlib.sha256(
                    doc.get("text", "").encode("utf-8")
                ).hexdigest(),
                doc.get("name", ""),
            )
            for doc_id, doc in documents.items()
            if doc.get("text")
        )
    )

    if not fingerprints:
        return None

    cache = st.session_state.get(
        "belleai_hybrid_index"
    )

    if (
        cache is not None
        and cache.get("fingerprints") == fingerprints
        and cache.get("index_version") == 2
    ):
        return cache

    chunks = []

    for doc_id in sorted(documents, key=str):
        document = documents[doc_id]

        if not document.get("text"):
            continue

        chunks.extend(
            chunk_document(
                text=document["text"],
                name=document.get(
                    "name",
                    "Document.pdf",
                ),
            )
        )

    if not chunks:
        return None

    model = get_embedding_model()

    # Normalize content before embedding so that
    # "topic1" and "topic 1" are represented similarly.
    embedding_texts = [
        normalize_text(chunk["text"])
        for chunk in chunks
    ]

    vectors = model.encode(
        embedding_texts,
        batch_size=32,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    token_counts = [
        Counter(tokenize(chunk["text"]))
        for chunk in chunks
    ]

    lengths = np.array(
        [
            sum(counts.values())
            for counts in token_counts
        ],
        dtype=float,
    )

    document_frequency = Counter()

    for counts in token_counts:
        document_frequency.update(counts.keys())

    cache = {
        "index_version": 2,
        "fingerprints": fingerprints,
        "chunks": chunks,
        "vectors": vectors,
        "token_counts": token_counts,
        "lengths": lengths,
        "doc_freq": document_frequency,
    }

    st.session_state[
        "belleai_hybrid_index"
    ] = cache

    return cache


def calculate_bm25_scores(
    question: str,
    index: dict,
) -> np.ndarray:
    """Calculate BM25 keyword relevance scores."""
    query_terms = set(tokenize(question))

    n = len(index["chunks"])

    scores = np.zeros(
        n,
        dtype=float,
    )

    if not query_terms:
        return scores

    average_length = max(
        float(np.mean(index["lengths"])),
        1.0,
    )

    k1 = 1.2
    b = 0.75

    for term in query_terms:
        df = index["doc_freq"].get(
            term,
            0,
        )

        if df == 0:
            continue

        idf = np.log(
            1.0
            + (n - df + 0.5)
            / (df + 0.5)
        )

        for i, counts in enumerate(
            index["token_counts"]
        ):
            tf = counts.get(
                term,
                0,
            )

            if tf == 0:
                continue

            length = index["lengths"][i]

            denominator = (
                tf
                + k1
                * (
                    1.0
                    - b
                    + b * length / average_length
                )
            )

            scores[i] += (
                idf
                * (tf * (k1 + 1.0))
                / denominator
            )

    return scores


def calculate_semantic_scores(
    question: str,
    index: dict,
) -> np.ndarray:
    """Calculate semantic similarity using embeddings."""
    model = get_embedding_model()

    normalized_question = normalize_text(
        question
    )

    query_vector = model.encode(
        [normalized_question],
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )[0]

    return np.asarray(
        index["vectors"] @ query_vector
    )


def reciprocal_rank_fusion(
    keyword_scores: np.ndarray,
    semantic_scores: np.ndarray,
    k: int = 60,
) -> np.ndarray:
    """
    Combine keyword and semantic rankings using RRF.

    Only positive keyword matches contribute to
    the keyword ranking.
    """
    n = len(keyword_scores)

    fused_scores = np.zeros(
        n,
        dtype=float,
    )

    semantic_order = np.argsort(
        -semantic_scores,
        kind="stable",
    )

    keyword_order = np.argsort(
        -keyword_scores,
        kind="stable",
    )

    # Semantic ranking
    for rank, index in enumerate(
        semantic_order
    ):
        fused_scores[index] += (
            1.0 / (k + rank + 1)
        )

    # Keyword ranking
    for rank, index in enumerate(
        keyword_order
    ):
        if keyword_scores[index] <= 0:
            break

        fused_scores[index] += (
            1.0 / (k + rank + 1)
        )

    return fused_scores


def select_diverse_chunks(
    chunks: list[dict],
    scores: np.ndarray,
    max_chunks: int = 5,
    max_chunks_per_page: int = 1,
) -> list[dict]:
    """
    Prefer evidence from different document pages.

    First select the strongest chunk from each page.
    If there are too few distinct pages, allow extra
    chunks from pages already selected.
    """
    ranked_indices = np.argsort(
        -scores,
        kind="stable",
    )

    selected = []
    selected_indices = set()
    page_counts = Counter()

    # First pass: prioritize different pages.
    for index in ranked_indices:
        index = int(index)

        chunk = chunks[index]

        page_key = (
            chunk["name"],
            chunk["page"],
        )

        if (
            page_counts[page_key]
            >= max_chunks_per_page
        ):
            continue

        selected.append(
            {
                **chunk,
                "score": float(scores[index]),
            }
        )

        selected_indices.add(index)
        page_counts[page_key] += 1

        if len(selected) >= max_chunks:
            return selected

    # Second pass: fill remaining slots if needed.
    for index in ranked_indices:
        index = int(index)

        if index in selected_indices:
            continue

        chunk = chunks[index]

        selected.append(
            {
                **chunk,
                "score": float(scores[index]),
            }
        )

        if len(selected) >= max_chunks:
            break

    return selected


def get_relevant_pages(
    question: str,
    documents: dict,
    max_pages: int = 5,
) -> list[dict]:
    """
    Retrieve PDF passages using hybrid RAG.

    Pipeline:
        1. Normalize question
        2. Retrieve keyword matches with BM25
        3. Retrieve semantic matches with embeddings
        4. Combine rankings with RRF
        5. Prefer distinct PDF pages
        6. Return evidence with page metadata
    """
    index = build_index(documents)

    if index is None:
        return []

    normalized_question = normalize_text(
        question
    )

    keyword_scores = calculate_bm25_scores(
        normalized_question,
        index,
    )

    semantic_scores = calculate_semantic_scores(
        normalized_question,
        index,
    )

    fused_scores = reciprocal_rank_fusion(
        keyword_scores,
        semantic_scores,
    )

    relevant_chunks = select_diverse_chunks(
        chunks=index["chunks"],
        scores=fused_scores,
        max_chunks=max_pages,
        max_chunks_per_page=1,
    )

    return relevant_chunks
