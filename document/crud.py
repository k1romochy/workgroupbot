from sqlalchemy import select
from core.models.document import Document
import core.models.db_helper as db


async def get_documents_url():
    async with db.async_session() as session:
        documents_url = await session.scalars(select(Document.url))

        return list(documents_url)


async def get_name_doc_by_url(url: str):
    async with db.async_session() as session:
        document_name = await session.scalar(select(Document).where(Document.url == url).order_by(Document.name))

        return document_name


async def get_doc_id_by_url(url: str):
    async with db.async_session() as session:
        document_id = await session.scalar(select(Document).where(Document.url == url).order_by(Document.id))

        return document_id


async def add_document(url: str, tg_id, name: str, term: int, type: str, registrated_at: str):
    async with db.async_session() as session:
        session.add(Document(url=url, tg_id=tg_id, name=name, term=term, type=type, registrated_at=registrated_at))

        await session.commit()


async def del_document_by_id(id: int):
    async with db.async_session() as session:
        document = await session.scalar(select(Document).where(Document.id == id))

        session.delete(document)
        await session.commit()


async def update_document_duration_by_id(id: int, plus_term: int):
    async with db.async_session() as session:
        document = await session.scalar(select(Document).where(Document.id == id))

        if document:
            new_term = int(document.term) + plus_term
            document.term = new_term

            await session.commit()
