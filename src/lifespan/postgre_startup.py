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

from sqlmodel import Session, SQLModel, select

from src.datamodels.embedded_model import Embedded
from src.dependencies.postgre_depedency import engine
from src.embeddings.embedder import embed
from src.env import CONTENT_SOURCES


def create_question_payload_chunks(file_path: Path, source_id: int) -> list[dict]:
    text = file_path.read_text(encoding="utf-8")
    url_match = re.match(r"URL: (.*)", text)
    url = url_match.group(1).strip() if url_match else ""
    content_str = ""
    separator = "---------------------------------------"
    if separator in text:
        content_str = text.split(separator, 1)[1].strip()
    else:
        content_str = "\n".join(text.splitlines()[1:]).strip()

    raw_blocks = re.split(r"\n(?=- )", content_str)
    processed_chunks = []
    for block in raw_blocks:
        parts = block.strip().split("\n", 1)
        if not parts:
            continue
        question = parts[0].strip().lstrip("- ").strip()
        payload = parts[1].strip() if len(parts) > 1 else ""
        if question:
            processed_chunks.append(
                {"source_id": source_id, "url": url, "question": question, "payload": payload}
            )
    return processed_chunks


@asynccontextmanager
async def lifespan(app):
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        for idx, source in enumerate(CONTENT_SOURCES):
            file_path: Path = source["path"]
            if not file_path.exists():
                continue

            chunks = create_question_payload_chunks(file_path, source_id=idx)

            for chunk_data in chunks:
                question = chunk_data["question"]
                statement = select(Embedded).where(
                    Embedded.source_id == idx, Embedded.question == question
                )
                if session.exec(statement).first():
                    continue

                full_context_text = f"{chunk_data['question']}\n{chunk_data['payload']}"

                vector = embed(full_context_text, task="passage")

                item = Embedded(
                    source_id=chunk_data["source_id"],
                    url=chunk_data["url"],
                    question=chunk_data["question"],
                    payload=chunk_data["payload"],
                    embedding=vector,
                )
                session.add(item)

        session.commit()

    yield
