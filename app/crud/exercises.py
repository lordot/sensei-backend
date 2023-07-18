from .base import CRUDBase
from ..models import Writing
from ..models.exercises import Reading
from ..schemas.exercises import WritingCreate, ReadingCreate

writing_crud = CRUDBase[Writing, WritingCreate, WritingCreate](Writing)
reading_crud = CRUDBase[Reading, ReadingCreate, ReadingCreate](Reading)


EX_TYPES = {
    'writing': writing_crud,
    'reading': reading_crud
}
