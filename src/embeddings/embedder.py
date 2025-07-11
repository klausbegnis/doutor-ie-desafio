"""
File: embedder.py
Project: embeddings
File Created: Friday, 11th July 2025 10:26:08 am
Author: Klaus Begnis (kbegnis23@gmail.com)
-----
Last Modified: Friday, 11th July 2025 10:26:10 am
Modified By: Klaus Begnis (kbegnis23@gmail.com>)
-----
Copyright (c) - Creative Commons Attribution 2025
"""

from sentence_transformers import SentenceTransformer

# modelo Sentence-Transformers do HuggingFace sem utilizacao de tokens API
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")


def embed(text: str) -> list[float]:
    text = text.strip().replace("\n", " ").replace("\r", " ")
    text = " ".join(text.split())
    return model.encode(text, convert_to_numpy=True, normalize_embeddings=True).tolist()
