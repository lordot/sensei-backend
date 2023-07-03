from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from ..models import ExWriting
from ..schemas.exercises import ExWritingCreate


class CRUDExWriting(CRUDBase[ExWriting, ExWritingCreate, ExWritingCreate]):

    async def get_random(
            self,
            session: AsyncSession,
            level: str = None
    ) -> ExWriting:
        stmt = select(ExWriting)
        if level:
            stmt = stmt.where(ExWriting.level == level)
        stmt = stmt.order_by(func.random())
        exercise = await session.execute(stmt)
        return exercise.scalars().first()


exwriting_crud = CRUDExWriting(ExWriting)

EX_TYPES = {
    'writing': exwriting_crud
}
