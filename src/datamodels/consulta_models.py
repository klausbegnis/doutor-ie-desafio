"""
File: consulta.py
Project: datamodels
File Created: Friday, 11th July 2025 10:01:40 am
Author: Klaus Begnis (kbegnis23@gmail.com)
-----
Last Modified: Friday, 11th July 2025 10:01:49 am
Modified By: Klaus Begnis (kbegnis23@gmail.com>)
-----
Copyright (c) - Creative Commons Attribution 2025
"""

from pydantic import BaseModel


class Consulta(BaseModel):
    """
    Consulta _summary_
    Base data model for the /consulta endpoint
    _extended_summary_

    question : str _description_ Questions received from user.

    Args:
        BaseModel (_type_): _description_
    """

    question: str


class SourceItem(BaseModel):
    """
    SourceItem _summary_

    Base model for wrapping embed value result
    _extended_summary_

    id : str _description_ Id from the document which the answer was retrieved.
    url : str _description_ Url from where the document is located.

    Args:
        BaseModel (_type_): _description_
    """

    id: str
    url: str


class ResponseItems(BaseModel):
    """
    ResponseItems _summary_

    Data object for each matching response.

    _extended_summary_

    payload : str _description_ Response fetched.
    sources : list[SourceItem] _description_ All SourceItems from the requested question.

    Args:
        BaseModel (_type_): _description_
    """

    payload: str
    sources: list[SourceItem]


class Response(BaseModel):
    """
    Response _summary_

    Data object wrapping all responses.

    _extended_summary_

    souces : list[ResponseItems] _description_ All responses fetched from model.

    Args:
        BaseModel (_type_): _description_
    """

    docs: list[ResponseItems]
