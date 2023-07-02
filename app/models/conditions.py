from sqlalchemy import Column, Enum, String


from ..core.db import Base
from .enums import Level, Type


class Condition(Base):
    level = Column(Enum(Level), nullable=False)
    type = Column(Enum(Type), nullable=True)
    text = Column(String(250), nullable=False, unique=True)
