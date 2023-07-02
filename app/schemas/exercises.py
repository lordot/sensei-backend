from typing import Optional, Union

from pydantic import BaseModel

from .conditions import ConditionRead
from ..models.exercises import Level


class ExWritingRead(BaseModel):
    id: str
    level: Level
    question: str

    class Config:
        orm_mode = True


class ExWritingCreate(BaseModel):
    level: Level
    question: str


class ExWritingUpdate(BaseModel):
    pass


class ExerciseWithConditions(BaseModel):
    exercise: ExWritingRead
    conditions: Optional[list[ConditionRead]]

    class Config:
        orm_mode = True
