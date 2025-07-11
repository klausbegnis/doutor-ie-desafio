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

from fastapi import APIRouter

from src.app.datamodels.consulta_models import Consulta, Response, ResponseItems, SourceItem

consulta_router = APIRouter()


@consulta_router.post("/consulta")
def request_consulta(consulta: Consulta) -> Response:
    """
    request_consulta _summary_

    _extended_summary_

    Args:
        consulta (Consulta): _description_

    Returns:
        Response : _description_
    """
    # question = consulta.question
    source_item = SourceItem(id="1", url="url")
    item = ResponseItems(payload="text", sources=[source_item])
    _res = Response(docs=[item])
    return _res
