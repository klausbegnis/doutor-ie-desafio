"""
File: dbitem_model.py
Project: datamodels
File Created: Friday, 11th July 2025 10:16:11 am
Author: Klaus Begnis (kbegnis23@gmail.com)
-----
Last Modified: Friday, 11th July 2025 10:16:13 am
Modified By: Klaus Begnis (kbegnis23@gmail.com>)
-----
Copyright (c) - Creative Commons Attribution 2025
"""

from typing import Annotated

from pgvector.sqlalchemy import Vector  # type: ignore
from sqlmodel import Column, Field, SQLModel


class Embedded(SQLModel, table=True):
    """
    Embedded _summary_

    Embedded data model for the emb function.
    At postgre a table called embedded is created when inserting the values
    into the database.

    _extended_summary_

    id: int | None = Field(default=None, primary_key=True)
    - key from the database table

    source_id: int = Field(index=True)
    - id from the sourced document

    url: str
    - url from the document

    question: str
    - question that must be searched for matching value

    payload: str
    - possible answer from the question

    embedding: Annotated[list[float], Field(sa_column=Column(Vector(1024)))]
    - the embedded payload

    Args:
        SQLModel (_type_): _description_
        table (bool, optional): _description_. Defaults to True.
    """

    id: int | None = Field(default=None, primary_key=True)
    source_id: int = Field(index=True)
    url: str
    question: str
    payload: str
    embedding: Annotated[list[float], Field(sa_column=Column(Vector(1024)))]
