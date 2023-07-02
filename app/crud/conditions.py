from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from ..models import Condition
from ..models.enums import Type, Level
from ..schemas.conditions import ConditionRead, ConditionCreate, ConditionUpdate


class CRUDCondition(CRUDBase[Condition, ConditionCreate, ConditionUpdate]):

    async def get_random(
            self,
            session: AsyncSession,
            count: int,
            level: Optional[Level] = None,
            conditions: Optional[list[Type]] = None
    ) -> list[Condition]:
        stmt = select(Condition).order_by(func.random())
        if conditions:
            stmt = stmt.filter(Condition.type.in_(conditions))
        if level:
            stmt = stmt.where(Condition.level == level)
        objects = await session.execute(stmt.limit(count))
        return objects.scalars().all()


condition_crud = CRUDCondition(Condition)
