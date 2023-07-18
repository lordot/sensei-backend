from typing import Optional, Union, TypeVar, Generic

from pydantic import BaseModel
from .conditions import ConditionRead
from ..models.exercises import Level

T = TypeVar('T')


class ExerciseRead(Generic[T], BaseModel):
    id: str
    level: Level

    class Config:
        orm_mode = True


class ExerciseCreate(Generic[T], BaseModel):
    level: Level


class ExerciseUpdate(BaseModel):
    pass


class ExerciseWithConditions(Generic[T], BaseModel):
    exercise: T
    conditions: Optional[list[ConditionRead]]

    class Config:
        orm_mode = True


class WritingRead(ExerciseRead):
    question: str


class WritingCreate(ExerciseCreate):
    question: str


class WritingWithConditions(ExerciseWithConditions[WritingRead]):
    pass


class ReadingRead(ExerciseRead):
    text: str


class ReadingCreate(ExerciseCreate):
    text: str


class ReadingWithConditions(ExerciseWithConditions[ReadingRead]):
    pass
