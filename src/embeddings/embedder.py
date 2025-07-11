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
model = SentenceTransformer("intfloat/multilingual-e5-large")


def embed(text: str, task: str = "passage") -> list[float]:
    """
    embed _summary_

    _extended_summary_

    Args:
        text (str): _description_
        task (str, optional): _description_. Defaults to "passage".

    Raises:
        ValueError: _description_

    Returns:
        list[float]: _description_
    """
    # the selected model requires a passage and a query
    if task not in ["passage", "query"]:
        raise ValueError("Task must be either 'passage' or 'query'")

    prefixed_text = f"{task}: {text}"
    prefixed_text = prefixed_text.strip().replace("\n", " ")
    prefixed_text = " ".join(prefixed_text.split())

    embedding = model.encode(
        prefixed_text, convert_to_numpy=True, normalize_embeddings=True
    ).tolist()

    return embedding  # type: ignore
