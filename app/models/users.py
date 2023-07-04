from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Enum, Integer

from .enums import Level
from ..core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    level = Column(Enum(Level), default=Level.A1, nullable=False)
    tokens = Column(Integer, default=0, nullable=True)

    def __repr__(self):
        return self.email
