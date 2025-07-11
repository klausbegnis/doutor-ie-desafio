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
    id: int | None = Field(default=None, primary_key=True)
    url: str
    content: str
    embedding: Annotated[list[float], Field(sa_column=Column(Vector(768)))]
