from sqlalchemy import select
from core.models.document import Document
import core.models.db_helper as db


async def get_documents_url():
    async with db.async_session() as session:
        documents_url = await session.scalars(select(Document.url))

        return list(documents_url)


async def get_name_doc_by_url(url):
    async with db.async_session() as session:
        document_name = await session.scalar(select(Document).where(Document.url == url).order_by(Document.name))


async def add_document(url, tg_id):
    async with db.async_session() as session:
        session.add(Document(url=url, tg_id=tg_id))

        await session.commit()
