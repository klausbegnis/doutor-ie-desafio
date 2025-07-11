"""
File: postgre_startup.py
Project: lifespan
File Created: Friday, 11th July 2025 10:30:36 am
Author: Klaus Begnis (kbegnis23@gmail.com)
-----
Last Modified: Friday, 11th July 2025 10:30:39 am
Modified By: Klaus Begnis (kbegnis23@gmail.com>)
-----
Copyright (c) - Creative Commons Attribution 2025
"""

from contextlib import asynccontextmanager

from sqlmodel import Session, SQLModel, select

from src.datamodels.embedded_model import Embedded
from src.dependencies.postgre_depedency import engine
from src.embeddings.embedder import embed
from src.env import CONTENT_SOURCES


# chunks basicos para primeiro test
def split_text(text: str) -> list[str]:
    blocks = []
    for line in text.splitlines():
        line = line.strip("–-• \t")
        blocks.append(line)
    return blocks


# cria o database caso nao exista e insere os documentos
@asynccontextmanager
async def lifespan(app):

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        for source in CONTENT_SOURCES:
            url = source["url"]
            path = source["path"]

            already_exists = session.exec(select(Embedded).where(Embedded.url == url)).first()
            if already_exists:
                print(f"[Ingest] Documentos já existem para: {url}")
                continue

            print(f"[Ingest] Inserindo documentos de: {path}")
            content = path.read_text(encoding="utf-8")
            for chunk in split_text(content):
                vector = embed(chunk)
                item = Embedded(url=url, content=chunk, embedding=vector)
                session.add(item)

        session.commit()

    yield  # aplicação inicia depois disso
