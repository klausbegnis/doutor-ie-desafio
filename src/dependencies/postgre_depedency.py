"""
File: postgre_depedency.py
Project: dependencies
File Created: Friday, 11th July 2025 10:10:30 am
Author: Klaus Begnis (kbegnis23@gmail.com)
-----
Last Modified: Friday, 11th July 2025 10:10:42 am
Modified By: Klaus Begnis (kbegnis23@gmail.com>)
-----
Copyright (c) - Creative Commons Attribution 2025
"""

from typing import Generator

from sqlmodel import Session, create_engine

from src.env import DATABASE_URL

engine = create_engine(DATABASE_URL)


def get_session() -> Generator[Session, None, None]:
    """
    get_session _summary_

    Generates a DB sesion using SQL Alchemy

    _extended_summary_

    Yields:
        Generator[Session, None, None]: _description_
    """
    with Session(engine) as session:
        yield session
