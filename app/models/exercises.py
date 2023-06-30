from sqlalchemy import Column, String, DateTime, Text, func, Enum

from .enums import Level
from ..core.db import Base


class Exercises(Base):
    __abstract__ = True
    level = Column(Enum(Level), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ExWriting(Exercises):
    question = Column(Text, nullable=False, unique=True)
