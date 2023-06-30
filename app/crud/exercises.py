from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from ..models import ExWriting
from ..schemas.exercises import ExWritingCreate


class CRUDExWriting(CRUDBase[ExWriting, ExWritingCreate, ExWritingCreate]):
    pass


exwriting_crud = CRUDExWriting(ExWriting)
