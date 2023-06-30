from sqlalchemy import Column, Integer, DateTime, Text, func

from ..core.db import Base


class Exercises(Base):
    __abstract__ = True
    level = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ExWriting(Exercises):
    question = Column(Text, nullable=False)
