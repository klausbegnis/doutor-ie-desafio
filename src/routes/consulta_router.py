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

from fastapi import APIRouter, Depends
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
    Performs a semantic search for a given question.

    Args:
        consulta (Consulta): The user's question.

    Returns:
        Response: A list of relevant documents.
    """
    question_vec = embed(consulta.question, task="query")  # embed the question

    results = session.exec(
        select(Embedded)
        .order_by(Embedded.embedding.cosine_distance(question_vec))  # type: ignore
        .limit(2)
    ).all()  # use the section - here we are limiting by the two best results
    # here is the follow up of the data models developed for this applicatoin
    response_items = []  # create the response items list
    for doc in results:
        sources = [SourceItem(id=str(doc.source_id), url=doc.url)]
        response_items.append(ResponseItems(payload=doc.payload, sources=sources))
    # return the Response object
    return Response(docs=response_items)
