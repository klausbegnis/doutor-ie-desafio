"""
File: consulta_router.py
Project: routes
File Created: Friday, 11th July 2025 10:03:15 am
Author: Klaus Begnis (kbegnis23@gmail.com)
-----
Last Modified: Friday, 11th July 2025 10:03:46 am
Modified By: Klaus Begnis (kbegnis23@gmail.com>)
-----
Copyright (c) - Creative Commons Attribution 2025
"""

from typing import Annotated

import numpy as np
from fastapi import APIRouter, Depends
from scipy.spatial.distance import cosine
from sqlmodel import Session, select

from src.datamodels.consulta_models import Consulta, Response, ResponseItems, SourceItem
from src.datamodels.embedded_model import Embedded
from src.dependencies.postgre_depedency import get_session
from src.embeddings.embedder import embed

consulta_router = APIRouter()


@consulta_router.post("/consulta")
def request_consulta(
    consulta: Consulta, session: Annotated[Session, Depends(get_session)]
) -> Response:
    """
    request_consulta _summary_

    _extended_summary_

    Args:
        consulta (Consulta): _description_

    Returns:
        Response : _description_
    """
    # question = consulta.question

    question_vec = embed(consulta.question)

    # query all documents with embeddings
    docs = session.exec(select(Embedded)).all()
    assert len(docs) > 0, "No documents found in DB"

    # calculate cosine similarity between question and each doc embedding
    def similarity(doc_vec):
        return 1 - cosine(question_vec, np.array(doc_vec))

    sims = [(doc, similarity(doc.embedding)) for doc in docs]

    # sort documents by descending similarity score
    sims.sort(key=lambda x: x[1], reverse=True)

    response_items = []
    for result in sims:
        if result[1] > 0.65:
            sources = []
            doc = result[0]
            _id = str(doc.id)
            source_item = SourceItem(id=_id, url=doc.url)
            sources.append(source_item)
            response_items.append(ResponseItems(payload=doc.content, sources=sources))

    _res = Response(docs=response_items)
    return _res
