"""
File: postgre_startup.py
Project: lifespan
File Created: Friday, 11th July 2025 10:30:36 am
Author: Klaus Begnis (kbegnis23@gmail.com)
-----
Last Modified: Friday, 11th July 2025 12:48:17 pm
Modified By: Klaus Begnis (kbegnis23@gmail.com>)
-----
Copyright (c) - Creative Commons Attribution 2025
"""

import re
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from sqlmodel import Session, SQLModel, select

from src.datamodels.embedded_model import Embedded
from src.dependencies.postgre_depedency import engine
from src.embeddings.embedder import embed
from src.env import CONTENT_SOURCES


def create_question_payload_chunks(file_path: Path, source_id: int) -> list[dict]:
    """
    create_question_payload_chunks _summary_

    _extended_summary_

    Args:
        file_path (Path): _description_
        source_id (int): _description_

    Returns:
        list[dict]: _description_
    """
    # read the data file
    text = file_path.read_text(encoding="utf-8")
    # extract the origin url from the documentation
    url_match = re.match(r"URL: (.*)", text)
    url = url_match.group(1).strip() if url_match else ""

    # isolates main content
    content_str = ""
    separator = "---------------------------------------"
    if separator in text:
        content_str = text.split(separator, 1)[1].strip()
    else:
        content_str = "\n".join(text.splitlines()[1:]).strip()
    # semantics division
    raw_blocks = re.split(r"\n(?=- )", content_str)  # divided pattern by ? or -
    processed_chunks = []
    # block processing
    for block in raw_blocks:
        # get first new line
        parts = block.strip().split("\n", 1)
        if not parts:
            continue
        # separates the question
        question = parts[0].strip().lstrip("- ").strip()
        # separates the content
        payload = parts[1].strip() if len(parts) > 1 else ""
        # append in the list of processed chunks
        if question:
            processed_chunks.append(
                {"source_id": source_id, "url": url, "question": question, "payload": payload}
            )
    return processed_chunks


@asynccontextmanager
async def lifespan(app: FastAPI):  # pylint: disable=unused-argument
    """
    _summary_

    Lifespan from the application.

    Ensures proper startup and finishing by creating the AsyncGenerator scope.

    Everything before yield is the startup, everyhing after yield is the clean up.

    This lifespan definition ensures that the database already contains the embed data model,
    otherwise initialize it.

    It also checks if all the data from /data is already in the database, otherwise adds it.

    _extended_summary_
    """

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # retrieve all data sources
        for idx, source in enumerate(CONTENT_SOURCES):
            file_path: Path = source["path"]
            if not file_path.exists():
                continue
            # create the data chunkgs withe the specified file
            chunks = create_question_payload_chunks(file_path, source_id=idx)
            # iterate with all created chunks
            for chunk_data in chunks:
                # embedded the values in the database
                question = chunk_data["question"]
                statement = select(Embedded).where(
                    Embedded.source_id == idx, Embedded.question == question
                )
                if session.exec(statement).first():
                    continue
                # embedded question with response
                full_context_text = f"{chunk_data['question']}\n{chunk_data['payload']}"

                vector = embed(full_context_text, task="passage")
                # create the data model
                item = Embedded(
                    source_id=chunk_data["source_id"],
                    url=chunk_data["url"],
                    question=chunk_data["question"],
                    payload=chunk_data["payload"],
                    embedding=vector,
                )
                # inser the item in the database
                session.add(item)
        # commit the section modifcations in a batch
        session.commit()
    # finished start up
    yield
    # clean up
