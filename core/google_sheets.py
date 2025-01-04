import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import gspread
from core.models.db_helper import async_session, engine
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()
DATABASE_URL = os.getenv('POSTGRES_URL')


async def fetch_data_from_db():
    async with async_session() as session:
        query = text("SELECT id, name, type, term, url, registrated_at FROM public.document;")
        result = await session.execute(query)
        rows = result.fetchall()
        return [tuple(row) for row in rows]


def update_google_sheet(data):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Документы").sheet1
    sheet.clear()
    for row in data:
        sheet.append_row(list(row))


async def export_to_google_sheets():
    data = await fetch_data_from_db()
    update_google_sheet(data)
