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
    question: str


class SourceItem(BaseModel):
    id: str
    url: str


class ResponseItems(BaseModel):
    payload: str
    sources: list[SourceItem]


class Response(BaseModel):
    docs: list[ResponseItems]
