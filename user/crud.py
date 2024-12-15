from sqlalchemy import select
from core.models.user import User
import core.models.db_helper as db


async def create_user(tg_id: int):
    async with db.async_session() as session:
        user: User = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()

