from datetime import datetime
from sqlalchemy import select

from core.models import User
from core.models.document import Document
import core.models.db_helper as db
from typing import List, Tuple


async def get_documents_url():
    async with db.async_session() as session:
        documents_url = await session.scalars(select(Document.url))

        return documents_url.all()


async def get_name_doc_by_url(url: str):
    async with db.async_session() as session:
        document_name = await session.scalar(select(Document.name).where(Document.url == url))

        return document_name


async def get_doc_id_by_url(url: str):
    async with db.async_session() as session:
        document_id = await session.scalar(select(Document.id).where(Document.url == url))

        return document_id


async def add_document(url: str, tg_id, name: str, term: int, type: str, registrated_at: str):
    async with db.async_session() as session:
        session.add(Document(url=url, tg_id=tg_id, name=name, term=term, type=type, registrated_at=registrated_at))

        await session.commit()


async def del_document_by_id(id: int):
    async with db.async_session() as session:
        document = await session.scalar(select(Document).where(Document.id == id))

        await session.delete(document)
        await session.commit()


async def update_document_duration_by_id(id: int, plus_term: int):
    async with db.async_session() as session:
        document = await session.scalar(select(Document).where(Document.id == id))

        if document:
            new_term = int(document.term) + plus_term
            document.term = new_term

            await session.commit()


async def delete_all_docs():
    async with db.async_session() as session:
        documents_url = await session.scalars(select(Document.url))

        for url in documents_url:
            document = await session.scalar(select(Document).where(Document.url == url))

            await session.delete(document)

        await session.commit()


async def update_documents():
    async with db.async_session() as session:
        documents = await session.scalars(select(Document))

        for document in documents:
            registrated_at_str = document.registrated_at
            registrated_at = datetime.strptime(registrated_at_str, "%Y_%m_%d")

            current_time = datetime.now()

            time_difference = current_time - registrated_at
            days_passed = time_difference.days

            if int(days_passed) > document.term:
                await session.delete(document)

        await session.commit()


async def add_time(document_id: int, plus_term: int):
    async with db.async_session() as session:
        document = await session.scalar(select(Document).where(Document.id == document_id))

        if document:
            new_term = int(document.term) + plus_term
            document.term = new_term

            await session.commit()


async def get_prosroki() -> List[Tuple[int, int]]:
    async with db.async_session() as session:
        documents = await session.scalars(select(Document))

        list_prosroki = []
        current_time = datetime.now()

        for document in documents:
            try:
                registrated_at = datetime.strptime(document.registrated_at, "%Y_%m_%d")
                time_difference = current_time - registrated_at
                days_passed = time_difference.days

                if days_passed > document.term:
                    diff = days_passed - document.term
                    list_prosroki.append((document.id, diff))
            except ValueError:
                continue

        return list_prosroki


async def get_url_by_id(doc_id: int):
    async with db.async_session() as session:
        document_url = await session.scalar(select(Document.url).where(Document.id==doc_id))

        return document_url


async def get_name_by_id(doc_id: int):
    async with db.async_session() as session:
        document_name = await session.scalar(select(Document.name).where(Document.id == doc_id))

        return document_name


async def get_term_diff_by_id(doc_id: int):
    async with db.async_session() as session:
        document = await session.scalar(select(Document).where(Document.id==doc_id))

        registrated_at_str = document.registrated_at
        registrated_at = datetime.strptime(registrated_at_str, "%Y_%m_%d")

        current_time = datetime.now()

        time_difference = current_time - registrated_at
        days_passed = time_difference.days

        result = int(document.term) - int(days_passed)

        return result
