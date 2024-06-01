from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def create_object(
            self,
            obj_in,
            user: Optional[User] = None,
    ):
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id

        return self.model(**obj_in_data)

    async def get_multi(
            self,
            session: AsyncSession,
            not_full_invested: bool = False
    ):
        query = select(self.model)
        if not_full_invested:
            query = query.where(~self.model.fully_invested)
        db_objs = await session.execute(query)
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None,
    ):
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id

        db_obj = self.model(**obj_in_data)

        # from app.services.charity_project import CharityProjectService
        # await CharityProjectService(session).add_to_queue(db_obj)

        await session.commit()
        await session.refresh(db_obj)

        return db_obj
